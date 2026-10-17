// LC0042: public WebKit DOM adapter. Uses only a nonpersistent website data store.
// Compile into target/ with explicit on-volume Swift/Clang module caches.
import AppKit
import Foundation
import WebKit

@MainActor
final class HeadingProbe: NSObject, WKNavigationDelegate {
    private let view: WKWebView
    private var completed = false

    override init() {
        let configuration = WKWebViewConfiguration()
        configuration.websiteDataStore = .nonPersistent()
        precondition(!configuration.websiteDataStore.isPersistent)
        view = WKWebView(frame: NSRect(x: 0, y: 0, width: 1024, height: 768),
                         configuration: configuration)
        super.init()
        view.navigationDelegate = self
    }

    func load(_ url: URL, root: URL) {
        if url.isFileURL {
            view.loadFileURL(url, allowingReadAccessTo: root)
        } else {
            view.load(URLRequest(url: url))
        }
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        Task { @MainActor in
            do {
                // A public async evaluation also lets short load-time callbacks finish.
                let value = try await webView.callAsyncJavaScript(
                    "await new Promise(resolve => setTimeout(resolve, 100)); " +
                    "return document.documentElement.outerHTML;",
                    arguments: [:], in: nil, contentWorld: .page)
                guard let dom = value as? String, !dom.isEmpty else {
                    self.fail("empty DOM result")
                    return
                }
                self.completed = true
                self.view.stopLoading()
                FileHandle.standardOutput.write(Data((dom + "\n").utf8))
                exit(0)
            } catch {
                self.fail("DOM evaluation: " + error.localizedDescription)
            }
        }
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        fail("navigation: " + error.localizedDescription)
    }

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!,
                 withError error: Error) {
        fail("provisional navigation: " + error.localizedDescription)
    }

    func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
        fail("WebKit content process terminated")
    }

    func fail(_ reason: String) {
        guard !completed else { return }
        completed = true
        view.stopLoading()
        FileHandle.standardError.write(Data(("WEBKIT-HEADING: REFUSED — " + reason + "\n").utf8))
        exit(2)
    }
}

@main
struct Driver {
    @MainActor
    static func main() {
        if CommandLine.arguments == [CommandLine.arguments[0], "--version"] {
            let bundle = Bundle(identifier: "com.apple.WebKit")
            let value: [String: Any] = [
                "engine": "WebKit",
                "version": bundle?.object(forInfoDictionaryKey: "CFBundleVersion") as? String ?? "unavailable",
                "os": ProcessInfo.processInfo.operatingSystemVersionString,
                "website_data": "nonpersistent"
            ]
            guard let data = try? JSONSerialization.data(withJSONObject: value, options: [.sortedKeys]) else {
                exit(2)
            }
            FileHandle.standardOutput.write(data + Data("\n".utf8))
            return
        }
        let environment = ProcessInfo.processInfo.environment
        guard CommandLine.arguments.count == 2,
              let suppliedRoot = environment["SEMULITH_PROBE_ROOT"],
              let url = URL(string: CommandLine.arguments[1]) else {
            FileHandle.standardError.write(Data("WEBKIT-HEADING: REFUSED — URL/root required\n".utf8))
            exit(2)
        }
        let root = URL(fileURLWithPath: suppliedRoot).resolvingSymlinksInPath()
        let allowedFile = url.isFileURL && url.resolvingSymlinksInPath().path.hasPrefix(root.path + "/target/")
        let allowedHTTP = url.scheme == "http" && ["127.0.0.1", "localhost"].contains(url.host ?? "")
        guard allowedFile || allowedHTTP else {
            FileHandle.standardError.write(Data("WEBKIT-HEADING: REFUSED — owned file or loopback URL required\n".utf8))
            exit(2)
        }
        let application = NSApplication.shared
        application.setActivationPolicy(.prohibited)
        let probe = HeadingProbe()
        probe.load(url, root: root.appendingPathComponent("target"))
        DispatchQueue.main.asyncAfter(deadline: .now() + 30) { probe.fail("load timeout") }
        withExtendedLifetime(probe) { application.run() }
    }
}
