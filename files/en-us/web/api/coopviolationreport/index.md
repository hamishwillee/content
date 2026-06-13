---
title: COOPViolationReport
slug: Web/API/COOPViolationReport
page-type: web-api-interface
browser-compat: api.ReportingObserver.ReportingObserver.options_parameter.types_property.coop
spec-urls:
  - https://html.spec.whatwg.org/multipage/browsers.html#embedder-policy-checks
  - https://html.spec.whatwg.org/multipage/browsers.html#coep
---

{{APIRef("Reporting API")}}

The `COOPViolationReport` dictionary of the [Reporting API](/en-US/docs/Web/API/Reporting_API) represents a report generated when a document violates its {{httpheader("Cross-Origin-Opener-Policy")}} (COOP), or a report-only policy set with {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}}.

Violation reports are sent for navigations that cause a browsing context group switch, severing communication with the opener.
For report-only policies, violation reports are sent for navigations that would cause a browsing context group switch and for window property accesses that would not have been possible had the policy been enforced.
This allows analysis and re-engineering of cross-window communication that COOP would break, before it is enabled.

The reports can be observed from within a page using a {{domxref("ReportingObserver")}} for access violations ([`access-to-opener`](#access-to-opener_report), but not for navigation violations ([`navigation-from-response`](#navigation-from-response_report) and [`navigation-to-response`](#navigation-from-response_report)).
A serialized version of `COOPViolationReport` can be sent to [reporting server endpoints](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints) for all these report types.

## Instance properties

- `body`
  - : The body of the report.
    This is an object with the following properties:
    - `type`
      - : A string representing the cause of the violation that triggered the report.
        This property is present in every report.

        The specification allows the following values:
        - [`navigation-from-response`](#navigation-from-response_report)
          - : Violation for the document being navigated from, if the destination document has an incompatible COOP.
            Chrome reports this type with this name.
        - [`navigation-to-response`](#navigation-to-response_report)
          - : Violation for the document being navigated to, when the previous document has an incompatible COOP.
            Chrome reports this type with this name.
        - `access-to-opener`
          - : (Report-only) Violation when a property access between the document and another window would have failed had the policy been enforced.
            The other window could be its opener, a window it opened, or another window in the browsing context group.
            The specification uses this single value for all six access scenarios (both directions, and all three window relationships), distinguishing them only by which properties are present in the body.
            Chrome does not emit this value: it reports these violations using the more granular `access-from-coop-page-to-*` and `access-to-coop-page-from-*` types listed below.

        Chrome additionally allows these types in reports for policies defined using `Cross-Origin-Opener-Policy-Report-Only`:
        - [`access-from-coop-page-to-opener`](#access-from-coop-page-to-opener_report)
          - : Generated for the COOP page when its script accesses a property on its opener window, where the policy would have disconnected them.
            Body includes `property`, `openerURL`, `referrer`, and `sourceFile`/`lineNumber`/`columnNumber`. Visible to ReportingObserver.
        - [`access-from-coop-page-to-openee`](#access-from-coop-page-to-openee_report)
          - : (Report-only) Generated for the COOP page when its script accesses a property on a window it opened, where the policy would have disconnected them.
            Body includes `property`, `openeeURL` (empty once the popup has navigated cross-origin), `initialPopupURL`, and `sourceFile`/`lineNumber`/`columnNumber`. Visible to ReportingObserver.
        - [`access-from-coop-page-to-other`](#access-from-coop-page-to-other_report)
          -: (Report-only) Generated for the COOP page when its script accesses a property on another window in the browsing context group (no opener relationship), where the policy would have disconnected them.
          Body includes `property` and `otherDocumentURL`, plus `sourceFile`/`lineNumber`/`columnNumber`.
          Visible to `ReportingObserver`.
        - [`access-to-coop-page-from-opener`](#access-to-coop-page-from-opener_report)
          - : (Report-only) Generated for the COOP page when its opener accesses a property on it, where the policy would have disconnected them.
            Body includes `property`, `openerURL`, and `referrer`.
            No source location (the accessing script ran in another page). Sent to reporting endpoints only.
        - [`access-to-coop-page-from-openee`](#access-to-coop-page-from-openee_report)
          - : (Report-only) Generated for the COOP page when a window it opened accesses a property on it, where the policy would have disconnected them.
            Body includes `property`, `openeeURL`, and `initialPopupURL`.
            No source location.
            Sent to reporting endpoints only.
        - [`access-to-coop-page-from-other`](#access-to-coop-page-from-other_report)
          - : (Report-only) Generated for the COOP page when another window in the browsing context group accesses a property on it, where the policy would have disconnected them.
            Body includes `property` and `otherDocumentURL`.
            No source location.
            Sent to reporting endpoints only.

    - `disposition`
      - : A string indicating whether the violation was enforced or only reported.
        This property is present in every type of COOP report.
        It can have one of the following values:
        - `"enforce"`
          - : The violation caused opening of the resource to be blocked.
            This is set for violations of policies set with {{httpheader("Cross-Origin-Opener-Policy")}}.
        - `"reporting"`
          - : The violation was reported without blocking the resource from opening.
            This is set for violations of policies set with {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}}.
    - `effectivePolicy`
      - : A string that indicates the effective COOP policy of the document for which the violation report is being sent (the policy value value that triggered the violation).
        Whether that policy is enforced or only reported against depends on the [`disposition`](#disposition).
        This property is present in every report.

        Note that this is the _effective policy_, not necessarily the literal policy that might (or might not) be sent with the document's response.
        For example, a document might not have any policy set, in which case its effective policy will be `"unsafe-none"`.

        Possible values are: [`"unsafe-none"`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy#unsafe-none), [`"same-origin"`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy#same-origin), [`"same-origin-allow-popups"`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy#same-origin-allow-popups), [`"noopener-allow-popups"`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy#noopener-allow-popups), and `"same-origin-plus-COEP"`.

        Note that the last value `"same-origin-plus-COEP"`does not have a corresponding COOP header string.
        This is sent when top level response hs both both `COOP: same-origin` and a cross-origin-isolating COEP (`require-corp` or `credentialless`).
        It matters when matching policies for deciding if the opened document should be in the same or a new BCG: a `same-origin` and `"same-origin-plus-COEP"` will end up in different BCGs, while two `same-origin` documents would have ended up in the same one!

    - `previousResponseURL` {{optional_inline}}
      - : A string indicating the sanitized URL of the document that was navigated from in a [`navigation-to-response`](#navigation-to-response_report) report.
        The URL is sanitized by removing the username, password, and URL fragment, if present.
        If the original "opener" document is not same-origin with the document that is navigated to, this is set to `null`.

    - `nextResponseURL` {{optional_inline}}
      - : A string indicating the sanitized URL of the opened document.
        This is reported for an opener document in a report with a [`body.type`](#type) of [`navigation-from-response`](#navigation-from-response_report).
    - `referrer` {{optional_inline}}
      - : A string representing Xxxxxx
        This is reported for an opener <!-- check --> document in a report with a [`body.type`](#type) of [`navigation-to-response`](#navigation-to-response) or [`access-to-opener`]().
    - `property` {{optional_inline}}
      - : A string representing whether XXXX
        This is reported for an opener <!-- check --> document in a report with a [`body.type`](#type) of [access-to-opened-window`](#access-to-opened-window) or [`access-to-opener`]().
    - `openerURL` {{optional_inline}}
      - : A string representing whether XXXX
        [`access-to-opener`](#access-to-opener)
    - `openedWindowURL` {{optional_inline}}
      - : A string representing whether XXXX
        [`access-to-opened-window`](#access-to-opened-window)
    - `openedWindowInitialURL` {{optional_inline}}
      - : A string representing whether XXXX
        [`access-to-opened-window`](#access-to-opened-window)
    - `sourceFile` {{optional_inline}}
      - : A string indicating the URL of the script that triggered the violation report.
        [`access-to-opener`](#access-to-opener), [`access-to-opened-window`](#access-to-opened-window)
    - `lineNumber` {{optional_inline}}
      - : A string indicating the line number in the script that triggered the violation report.
        [`access-to-opener`](#access-to-opener), [`access-to-opened-window`](#access-to-opened-window)
    - `columnNumber` {{optional_inline}}
      - : A string indicating the column number in the script that triggered the violation report.
        [`access-to-opener`](#access-to-opener), [`access-to-opened-window`](#access-to-opened-window)

- `type`
  - : The string `"coop"`, indicating that this is a COOP violation report.

- `url`
  - : A string representing the URL of the document that generated the report.

## Description

When navigating to a new document, or using {{domxref("window.open()")}} to open a document, the new document may be opened in the same {{glossary("Browsing context","browsing context group (BCG)")}} as the original document, or in a new BCG.
If a document is opened in a new BCG, the two documents are isolated from each other: window handles referencing the other document (such as `window.opener` or the return value of `window.open()`) are severed, closing a number of paths by which a malicious document might otherwise interact with documents it opens or that open it.

Whether or not a document is opened in a new BCG depends on whether it is same-origin or cross-origin with the original document, and the {{httpheader("Cross-Origin-Opener-Policy")}} of both documents.
In other words, a document's policy defines the policy (or policies) that other documents must have in order to open or navigate to the document in the same BCG, and in order to be opened or navigated from this document and remain in the same BCG.
Document policies may be set and enforced using the {{httpheader("Cross-Origin-Opener-Policy")}} HTTP header.

The {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}} header can be used to test the effect of enforcing a COOP policy for a particular document.
When the document opens or is opened by another document, its reporting-only policy is compared to the policy of the other document to determine if there would be a violation and send an appropriate report.
A document can set `Cross-Origin-Opener-Policy` and/or `Cross-Origin-Opener-Policy-Report-Only` headers.
These can have the same or different policies and reporting endpoints.

Violations are reported using the [Reporting API](/en-US/docs/Web/API/Reporting_API) whenever a policy causes (or, would cause, for report-only policies) a document to be opened in a new BCG.
For report-only policies, violations are also reported for attempted accesses between the document and other documents in the BCG (its opener, documents it opened, or others) that would have failed had the policy been enforced.
This allows analysis and re-engineering of cross-window communication that COOP would break, before it is enabled.

Reports for accesses made from the document can be returned via the {{domxref("ReportingObserver")}} interface in a `COOPViolationReport` object (navigation reports, and reports for accesses made to the document from other documents, are only sent to reporting server endpoints).

`COOPViolationReport` reports can also be serialized and sent in a `POST` to a [reporting server endpoint](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints).
To send to a reporting server endpoint the {{httpheader("Cross-Origin-Opener-Policy")}} and/or {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}} headers used to set the policy must include the `report-to` parameter with a valid reporting endpoint name.
Valid endpoint names to URL mappings are defined using the {{httpheader("Reporting-Endpoints")}} header.

### Types of COOP reports

Different reports are sent depending on whether the reporter is the opener or opened document in a navigation, or if the report is for a COOP access violation.
The types of these reports is indicated by the [`body.type](#type) property (the {{domxref("Report.type")}} is`coop` for all of these).

While all the COOP reports can be sent to [reporting server endpoints](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints), only access violation reports ([`access-to-opener`](#access-to-opener_report)) can be sent to an in-page {{domxref("ReportingObserver")}} (the navigation reports cannot).

#### `navigation-to-response` report

<!-- navigation-to-response - Fired on the page being navigated to when the incoming document has an incompatible COOP. -->

This type of report is sent to the COOP reporting endpoint, if specified, of a document that is navigated-to (pened) in a navigation.

For an enforced COOP policy, it indicates that the document was opened in a new BCG.
This occurs when the COOP policy of the opened document is incompatible with that of its opener.
For navigations this means that the opened document has a different COOP policy from its opener, or the same policy but they are not same-site (unless both documents have a COOP policy of [`unsafe-none`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy#unsafe-none)).

For a report-only COOP policy, it indicates the report-only COOP policy is incompatible with the (enforced) policy of its opener.
In other words, that the report-only policy set in `Cross-Origin-Opener-Policy-Report-Only` would result in a violation if it was enforced.

The report has the following body properties:

- `type`: `"navigation-to-response"`
- `disposition`: Whether the report is for an `"enforced"` or `"reporting"` policy.
- `effectivePolicy`: The effective policy of the opened document.
- `previousResponseURL`: The sanitized URL of the previous document (that was navigated from), or `null` for cross-origin navigations.
  This is the URL of the opener.
  It might be the same URL as the {{domxref("COOPViolationReportBody.referrer","referrer")}} or it might be an intermediate redirect URL.
- `referrer`: The original URL that started the navigation chain that resulted in this report.

<!--

navigation-to-response is the report type generated for the destination of the navigation. It means: "a browsing context navigated to this response, and this response's COOP forced (or would force) it into a new browsing context group, breaking the link to the previous document/opener." It's the mirror of navigation-from-response, which is sent on behalf of the document being navigated away from. So if page A (with COOP reporting configured) navigates to page B (also with COOP reporting configured), A's endpoint can receive a navigation-from-response report and B's endpoint a navigation-to-response report.
previousResponseURL is a field in the navigation-to-response report body. It's the URL of the response that occupied the browsing context before the navigation — i.e., the page you came from. To avoid leaking cross-origin browsing history, it's only populated when the previous response is same-origin with the response that's doing the reporting; otherwise it's an empty string. (The navigation-from-response report has the symmetric field, nextResponseURL, with the same same-origin condition.) A typical body looks like:
json{
  "type": "coop",
  "url": "https://example.com/page",
  "body": {
    "disposition": "enforce",
    "effectivePolicy": "same-origin",
    "previousResponseURL": "https://example.com/start",
    "referrer": "https://example.com/start"
  }
}
Sanitization of URLs in these reports follows the spec's "sanitize a URL to send in a report" algorithm, which does two things before serializing the URL:

Strips credentials — the username and password (userinfo) components are emptied.
Strips the fragment — the URL is serialized with the exclude fragment flag, so anything after # is dropped.

Everything else, including the path and query string, is kept intact. The same sanitization applies to the report's own url field and to nextResponseURL, not just previousResponseURL — the same-origin check is a separate, additional restriction layered on top of it for the previous/next response URLs.

-->

#### `navigation-from-response` report

<!-- navigation-from-response:  Fired on the page being navigated away from when the new document has an incompatible COOP. -->

This type of report is sent to the COOP reporting endpoint, if specified, of an document that is navigated-from in a navigation.

For navigations this means that the opened document has a different COOP policy from its opener, or the same policy but they are not same-site (unless both documents have a COOP policy of [`unsafe-none`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy#unsafe-none)).

For a report-only COOP policy, it indicates the report-only COOP policy of the opener is incompatible with the (enforced) policy of the page that is being navigated to.
In other words, that the report-only policy set in `Cross-Origin-Opener-Policy-Report-Only` would result in a violation if it was enforced.

Report of type `navigation-from-response` have the following body properties

- [`type`](#type): `navigation-from-response`
- [`disposition`](#disposition): Whether the report is for an `enforced` or `reporting` policy.
- [`effectivePolicy`](effectivepolicy): The policy of the opener document.
- [`nextResponseURL`](#nextresponseurl): The sanitized URL of the opened document (that was navigated to), or `null` for cross origin navigations.

#### `access-to-opener` report

This type of report is generated, for policies defined using `Cross-Origin-Opener-Policy-Report-Only`, when a property access between the document and another window would have failed had the policy been enforced.
The other window could be its opener, a window it opened, or another window in the browsing context group.
The access can also be in either direction.

The specification uses this single report type for all six access scenarios distinguishing them only by which properties are present in the body (Chrome reports these violations using the more granular `access-from-coop-page-to-*` and `access-to-coop-page-from-*` types.)

| Spec algorithm | Body signature | Chrome type |
| -------------- | -------------- | ----------- |

| access to an opened window | `openedWindowURL`, `openedWindowInitialURL`, **+source position** | `access-from-coop-page-to-openee` |
| access to another window | `otherURL`, **+source position** | `access-from-coop-page-to-other` |
| access from the opener | `openerURL`, `referrer`, **no source position** | `access-to-coop-page-from-opener` |
| access from an opened window | `openedWindowURL`, `openedWindowInitialURL`, **no source position** | `access-to-coop-page-from-openee` |
| access from another window | `otherURL`, **no source position** | `access-to-coop-page-from-other` |

##### access to the opener (`access-from-coop-page-to-opener`)

https://html.spec.whatwg.org/multipage/browsers.html#coop-violation-access-to-opener

The report has the following body properties:

- `type`: `"access-to-opener"`
- `disposition`: `"reporting"`
- `effectivePolicy`: The effective policy of the opened document. <!-- Check this spec says coop's report-only value -->
- `property propertyName` <!-- don't know what this means, check spec -->
- `openerURL`: If coopOrigin and openerOrigin are same origin, this is the sanitization of openerURL, null otherwise.
- `referrer`: serializedReferrer - The original URL that started the navigation chain that resulted in this report.
- `sourceFile` sourceFile
- `lineNumber` lineNumber
- `columnNumber` columnNumber

<!-- Check all above. Get an actual report to see what is sent -->

<!--

Yes — the mapping is exactly one-to-one. The spec has six distinct queuing algorithms and Chrome has six type strings, and they pair up cleanly. What collapses in the spec is only the `type` label, so to recover the Chrome type from a spec `access-to-opener` body you need two discriminators:

**Direction** — presence of the source-position fields. The three "access made by the COOP page's own script" algorithms include `sourceFile`/`lineNumber`/`columnNumber`; the three "someone accessed the COOP page" algorithms omit them (the script ran in another document, so exposing its position would leak).

**Relationship** — which URL key the body carries: `openerURL` (opener), `openedWindowURL` + `openedWindowInitialURL` (openee; Chrome's `openeeURL`/`initialPopupURL`), or `otherURL` (other; Chrome's `otherDocumentURL`).

Giving:

(Note the inversion hazard in the names: the spec's "access **to** the opener" is Chrome's "access-**from**-coop-page-to-opener" — the spec names algorithms from the access's perspective, Chrome's types from the COOP page's. The shared spec type string `access-to-opener` matches only the first row's semantics; for the other five it's just a label.)

Two caveats on whether the body-signature discrimination is *reliable*, as opposed to merely defined:

1. **Source position can theoretically be absent.** The explainer conditions those fields on the UA being able to extract a script position, and the spec's "let sourceFile... be the relevant script URL" presumes one exists. If an access-from-page report ever lacked them (access triggered outside an extractable script context), it would become byte-identical in shape to the corresponding access-to-page report. Chrome's explicit type strings are immune to this; the spec encoding isn't.

2. **Withheld URLs.** Under Chrome's convention the key stays present as `''`, so relationship discrimination survives sanitization. Under a literal reading of the spec's "null otherwise," an implementation that *omitted* null members would produce, e.g., an other-window report with no URL key at all — at which point `otherURL`-vs-`openerURL` discrimination fails too (though the openee case keeps a `referrer`-vs-nothing distinction, and opener-direction reports keep `referrer`). This is hypothetical since Chrome is the only implementation, but it means the spec's collapsed type is only losslessly recoverable given Chrome-style serialization.

So for your docs: it's accurate to say the spec's `access-to-opener` covers exactly the six Chrome types, that the Chrome type can in principle be derived from a spec-shaped body via "which URL field + whether source-position fields are present," and that Chrome simply pre-computes that classification into the `type` string.

-->

  <!-- access-to-opener:   Fired when a page accesses a property on its cross-origin opener window. Visible to ReportingObserver. -->

- disposition
- effectivePolicy
- type

- property
- openerURL

sourceFile
lineNumber
columnNumber

--

t body be a new object containing the following properties:

key value
type "access-to-opener"

property propertyName
referrer serializedReferrer

sourceFile sourceFile
lineNumber lineNumber
columnNumber columnNumber

Queue body as "coop" for coop's reporting endpoint with coopURL and environment.

To queue a violation report for access to an opened window, given an opener policy coop, three URLs coopURL, openedWindowURL and initialWindowURL, three origins coopOrigin, openedWindowOrigin, and openerInitialOrigin, a string propertyName, and an environment settings object environment:

Let sourceFile, lineNumber, and columnNumber be the relevant script URL and problematic position which triggered this report.

Let body be a new object containing the following properties:

key value
disposition "reporting"
effectivePolicy coop's report-only value
type "access-to-opener"

property propertyName
openedWindowURL If coopOrigin and openedWindowOrigin are same origin, this is the sanitization of openedWindowURL, null otherwise.
openedWindowInitialURL If coopOrigin and openerInitialOrigin are same origin, this is the sanitization of initialWindowURL, null otherwise.

sourceFile sourceFile
lineNumber lineNumber
columnNumber columnNumber

#### `access-from-coop-page-to-opener` report

Chrome only, from explainer. Also tested in WPT.

Report-only. Generated for the COOP page when its script accesses a property on its opener window, where the policy would have disconnected them. Body includes `property`, `openerURL`, `referrer`, and `sourceFile`/`lineNumber`/`columnNumber`. Visible to ReportingObserver.

#### `access-from-coop-page-to-openee` report

Chrome only, from explainer

Report-only. Generated for the COOP page when its script accesses a property on a window it opened, where the policy would have disconnected them. Body includes `property`, `openeeURL` (empty once the popup has navigated cross-origin), `initialPopupURL`, and `sourceFile`/`lineNumber`/`columnNumber`. Visible to ReportingObserver.

#### `access-from-coop-page-to-other` report

Chrome only, from explainer

Report-only. Generated for the COOP page when its script accesses a property on another window in the browsing context group (no opener relationship), where the policy would have disconnected them. Body includes `property` and `otherDocumentURL`, plus `sourceFile`/`lineNumber`/`columnNumber`. Visible to ReportingObserver.

#### `access-to-coop-page-from-opener` report

Chrome only, from explainer

Report-only. Generated for the COOP page when its opener accesses a property on it, where the policy would have disconnected them. Body includes `property`, `openerURL`, and `referrer`. No source location (the accessing script ran in another page). Sent to reporting endpoints only.

#### `access-to-coop-page-from-openee` report

Chrome only, from explainer

Report-only. Generated for the COOP page when a window it opened accesses a property on it, where the policy would have disconnected them. Body includes `property`, `openeeURL`, and `initialPopupURL`. No source location. Sent to reporting endpoints only.

#### `access-to-coop-page-from-other` report

Chrome only, from explainer

Report-only. Generated for the COOP page when another window in the browsing context group accesses a property on it, where the policy would have disconnected them. Body includes `property` and `otherDocumentURL`. No source location. Sent to reporting endpoints only.

**Accesses made _from_ the COOP page** (the page's own script reaching across the virtual BCG boundary — these are the ones that also notify `ReportingObserver`s, and the only ones carrying `sourceFile`/`lineNumber`/`columnNumber`):

| Type                              | Counterpart window        | Distinctive body fields        |
| --------------------------------- | ------------------------- | ------------------------------ |
| `access-from-coop-page-to-opener` | its opener                | `openerURL`, `referrer`        |
| `access-from-coop-page-to-openee` | a window it opened        | `openeeURL`, `initialPopupURL` |
| `access-from-coop-page-to-other`  | another window in the BCG | `otherDocumentURL`             |

**Accesses made _to_ the COOP page** (another window's script touching the COOP page — endpoint-only, no source position fields since the script ran in someone else's page):

| Type                              | Counterpart window        | Distinctive body fields        |
| --------------------------------- | ------------------------- | ------------------------------ |
| `access-to-coop-page-from-opener` | its opener                | `openerURL`, `referrer`        |
| `access-to-coop-page-from-openee` | a window it opened        | `openeeURL`, `initialPopupURL` |
| `access-to-coop-page-from-other`  | another window in the BCG | `otherDocumentURL`             |

All six share `disposition` (always `"reporting"` — access reports are report-only-only), `effectivePolicy` (the report-only value), and `property` (the window property touched). The URL fields are sanitized and subject to the same-origin conditions, empty string otherwise — openerURL is reported only if the COOP document and its whole redirect chain are same-origin with the opener; openeeURL only if the opened document and its redirects are same-origin with the COOP document; initialPopupURL only if the COOP document is same-origin with the popup creator; otherDocumentURL only if both documents and both redirect chains are all same-origin. (`initialPopupURL` is reportable more liberally because the COOP page, as the opener, initiated that navigation and already knew the URL.)

Two caveats worth noting if you're documenting these:

1. **Field-name drift.** The explainer puts the type string in a field named _violation_, but what Chrome actually ships puts it in the standard Reporting API `type` field of the body. Likewise the explainer's navigation values were "navigate-to-document"/"navigate-from-document", whereas Chrome ships the spec's `navigation-to-response`/`navigation-from-response`. So for the navigation reports the spec and Chrome agree; only the access types are Chrome-specific (the spec, as we established, labels all six access bodies `access-to-opener`).

2. **Counterpart fields differ from spec naming too.** The spec's access bodies use `openedWindowURL`/`openedWindowInitialURL` where the explainer/Chrome use `openeeURL`/`initialPopupURL`. If your `COOPViolationReport` page lists fields, you'll need to pick a source of truth and verify against actual Chrome report payloads — given the spec's editorial state here, observed Chrome output is probably the more useful reference for readers, with spec divergences either noted or ignored.

<!-- From the COEP doc -->

<!--

A document's policies for loading and embedding cross-origin resources that are requested in `no-cors` mode are configured and enforced using the {{httpheader("Cross-Origin-Embedder-Policy")}} HTTP header, and may also be reported but not enforced using the {{httpheader("Cross-Origin-Embedder-Policy-Report-Only")}} header.

You can monitor for COEP violation reports within the page that sets the policy using the [Reporting API](/en-US/docs/Web/API/Reporting_API).
To do this you create a {{domxref("ReportingObserver")}} object to listen for reports, passing a callback method and an (optional) `options` property specifying the types of reports that you want to report on.
The callback method is then called with reports of the requested types, passing a report object.
For COEP violations, the object will be a `COEPViolationReport` (which has the [`type`](#type) property set to `"coep"`).

The structure of a typical report is shown below.
Note that we can see the URL of both the page that had its policy violated (`url`) and the resource that was blocked from loading (`body.blockedURL`).
We can also see that the report was triggered by a `corp` violation, and from the `body.disposition` that it was enforced (and not just reported).

```json
{
  "type": "coep",
  "url": "https://url-of-page-attempting-to-load-resource-in-violation",
  "body": {
    "type": "corp",
    "blockedURL": "https://url-of-blocked-resource",
    "destination": "image",
    "disposition": "enforce"
  }
}
```

Violation reports may also be sent as a JSON object in a `POST` to a configured [reporting server endpoint](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints).
The reporting server endpoint name is specified in the [`report-to`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy#report-to_endpoint_name) policy directive of the {{httpheader("Cross-Origin-Embedder-Policy")}} or {{httpheader("Cross-Origin-Embedder-Policy-Report-Only")}} header.
Valid endpoint names and their mapping to a particular URL are defined using the {{httpheader("Reporting-Endpoints")}} header.

The structure of the server report is almost exactly the same as `COEPViolationReport`, except that it additionally includes `age` and `user_agent` fields.

```json
[
  {
    "age": 967132,
    "body": {
      "blockedURL": "https://url-of-resource-that-was-blocked",
      "destination": "image",
      "disposition": "enforce",
      "type": "corp"
    },
    "type": "coep",
    "url": "https://url-of-document-that-generated-report",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
  }
]
```

----

## Examples

### Using the `ReportingObserver` interface

This example shows how you can obtain COEP violation reports using a {{domxref("ReportingObserver")}}.

First consider the case where we have an HTML file hosted on the origin `https://example.com`, which includes an {{htmlelement("img")}} element that sets as its source the (cross-origin) resource `some-image.png`.
Since the element does not set the [`crossorigin`](/en-US/docs/Web/HTML/Reference/Attributes/crossorigin) attribute, it will be requested in `no-cors` mode.
By default, if `some-image.png` is not served with the {{httpheader("Cross-Origin-Embedder-Policy")}} header, this request will succeed.

```html
<img src="https://another-example.com/some-image.png" />
```

In order to ensure that the document only loads cross-origin resources that indicate that they are safe to load in our document origin, we can set the {{httpheader("Cross-Origin-Embedder-Policy")}} header with the [`require-corp`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy#require-corp) directive as shown:

```http
Cross-Origin-Embedder-Policy: require-corp
```

This header enforces that all resources must be served with the {{HTTPHeader("Cross-Origin-Resource-Policy")}} header and a value of `cross-origin` in order to be loaded into the document's origin (`https://example.com`).
Provided the server hosting `some-image.png` doesn't set the header, we don't need to do anything else to trigger a COEP violation.

To observe violations within the page, we construct a new {{domxref("ReportingObserver")}} object to listen for reports with the type `"coep"`, passing a callback that will receive and log the reports.
This code needs to be loaded before the script that causes the violation:

```js
const options = {
  types: ["coep"],
  buffered: true,
};

const observer = new ReportingObserver((reports, observer) => {
  reports.forEach((violation) => {
    console.log(violation);
    console.log(JSON.stringify(violation));
  });
}, options);

observer.observe();
```

Above, we log each violation report object and a JSON-string version of the object, which might look similar to the object below.
Note that the `type` is `"coep"`.

```json
{
  "type": "coep",
  "url": "https://example.com",
  "body": {
    "type": "corp",
    "blockedURL": "https://another-example.com/some-image.png",
    "destination": "image",
    "disposition": "enforce"
  }
}
```

The same report could be generated using {{httpheader("Cross-Origin-Embedder-Policy-Report-Only")}}, except that the [disposition](#disposition) would be reported as `"reporting"`.

### Sending a report to a reporting endpoint

Configuring a web page to send a COEP report to a [reporting server endpoint](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints) is almost the same as the previous example.
The only difference is that we need to specify a reporting endpoint where we want the reports to be sent, using the {{httpheader("Reporting-Endpoints")}} response header, and then reference these in the `report-to` parameter when setting the policy.

You can see this below, where we define the endpoint named `coep-endpoint` and then reference it in our policy:

```http
Reporting-Endpoints: coep-endpoint="https://some-example.com/coep"
Cross-Origin-Embedder-Policy: require-corp; report-to="coep-endpoint"
```

The violation report will then be sent as a JSON object in a `POST` to the endpoint referenced by `coep-endpoint`.

The report object has the same structure as returned from the `ReportingObserver` callback except for the addition of `age` and `user_agent` properties.

```json
[
  {
    "age": 717139,
    "body": {
      "blockedURL": "https://another-example.com/some-image.png",
      "destination": "image",
      "disposition": "enforce",
      "type": "corp"
    },
    "type": "coep",
    "url": "https://example.com",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
  }
]
```

The same report would be generated if we set {{httpheader("Cross-Origin-Embedder-Policy-Report-Only")}} in the same way, except that the [disposition](#disposition) would be set to `"reporting"`.

-->

<!-- BELOW HERE IS THE NEW OLD DOC WE WANT TO INTEGRATE -->

<!--

--
Examples

# COEP report

this example we create a new {{domxref("ReportingObserver")}} to observe COOP reports, then log the first report to the console.

`js
nst options = {
types: ["coop"],
buffered: true,
const observer = new ReportingObserver((reports, observer) => {
const firstReport = reports[0];
console.log(firstReport.type); // coop
console.log(firstReport);
}, options);

````

The logged report object for a COOP violation from loading an iframe might look like this:

```json

````

-->

<!--
Reports

[0] --- New Report Received [4:19:42 pm] ---
[0] [
[0]   {
[0]     age: 1,
[0]     body: {
[0]       disposition: 'reporting',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]

[
  {
    "type": "coop-access-violation",
    "url": "https://localhost:8443/",
    "body": {
      "sourceFile": "https://localhost:8443/",
      "lineNumber": 79,
      "columnNumber": 38,
      "type": "access-from-coop-page-to-openee",
      "property": "closed",
      "openeeURL": ""
    }
]

[0]
[0] --- New Report Received [3:21:17 pm] ---
[0] [
[0]   {
[0]     age: 40893,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 4876,
[0]     body: {
[0]       columnNumber: 44,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:9443/',
[0]       lineNumber: 283,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:22:17 pm] ---
[0] [
[0]   {
[0]     age: 3217,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:23:17 pm] ---
[0] [
[0]   {
[0]     age: 4932,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:23:17 pm] ---
[0] [
[0]   {
[0]     age: 4943,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:24:17 pm] ---
[0] [
[0]   {
[0]     age: 49652,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]       lineNumber: 311,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 29730,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:8443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:24:17 pm] ---
[0] [
[0]   {
[0]     age: 7133,
[0]     body: {
[0]       disposition: 'enforce',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/enforce-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:25:17 pm] ---
[0] [
[0]   {
[0]     age: 16064,
[0]     body: {
[0]       disposition: 'enforce',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/enforce-same-origin/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:25:17 pm] ---
[0] [
[0]   {
[0]     age: 53429,
[0]     body: {
[0]       disposition: 'enforce',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/enforce-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 26600,
[0]     body: {
[0]       disposition: 'enforce',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/enforce-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:26:17 pm] ---
[0] [
[0]   {
[0]     age: 16813,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 13480,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       lineNumber: 311,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 8864,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       nextResponseURL: 'https://localhost:8443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:26:17 pm] ---
[0] [
[0]   {
[0]     age: 16824,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:26:26 pm] ---
[0] [
[0]   {
[0]     age: 8,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       previousResponseURL: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'navigation-to-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:27:17 pm] ---
[0] [
[0]   {
[0]     age: 47435,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       openerURL: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       property: 'location',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-to-coop-page-from-opener'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:27:17 pm] ---
[0] [
[0]   {
[0]     age: 28002,
[0]     body: {
[0]       columnNumber: 44,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-plus-coep',
[0]       initialPopupURL: 'https://localhost:9443/',
[0]       lineNumber: 283,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin-plus-coep/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-plus-coep/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 31969,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-plus-coep',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-plus-coep/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:27:17 pm] ---
[0] [
[0]   {
[0]     age: 39335,
[0]     body: {
[0]       columnNumber: 24,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       lineNumber: 304,
[0]       openeeURL: '',
[0]       property: 'location',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 39312,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 50795,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       nextResponseURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 47415,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 47435,
[0]     body: {
[0]       columnNumber: 24,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       lineNumber: 304,
[0]       openeeURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       property: 'location',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 37872,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       lineNumber: 311,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:28:17 pm] ---
[0] [
[0]   {
[0]     age: 710,
[0]     body: {
[0]       disposition: 'enforce',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/enforce-same-origin-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [3:28:17 pm] ---
[0] [
[0]   {
[0]     age: 46659,
[0]     body: {
[0]       disposition: 'enforce',
[0]       effectivePolicy: 'same-origin-plus-coep',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/enforce-same-origin-plus-coep/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]

[1] {"level":"info","ts":1781312073.120943,"msg":"autosaved config (load with --resume flag)","file":"C:\\Users\\hamis\\AppData\\Roaming\\Caddy\\autosave.json"}
[1] {"level":"info","ts":1781312073.120943,"msg":"serving initial configuration"}
[0]
[0] --- New Report Received [10:56:10 am] ---
[0] [
[0]   {
[0]     age: 4895,
[0]     body: {
[0]       columnNumber: 44,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:9443/',
[0]       lineNumber: 343,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 13051,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:57:10 am] ---
[0] [
[0]   {
[0]     age: 8748,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 46426,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 1000,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 3412,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]       lineNumber: 385,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:57:10 am] ---
[0] [
[0]   {
[0]     age: 8757,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:58:10 am] ---
[0] [
[0]   {
[0]     age: 3425,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:58:10 am] ---
[0] [
[0]   {
[0]     age: 3411,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:58:10 am] ---
[0] [
[0]   {
[0]     age: 59601,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]       lineNumber: 385,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 58744,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 51648,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin',
[0]       nextResponseURL: 'https://localhost:8443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:58:15 am] ---
[0] [
[0]   {
[0]     age: 13,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       previousResponseURL: '',
[0]       referrer: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       type: 'navigation-to-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:58:39 am] ---
[0] [
[0]   {
[0]     age: 7,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       previousResponseURL: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'navigation-to-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:59:00 am] ---
[0] [
[0]   {
[0]     age: 14,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       previousResponseURL: '',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'navigation-to-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:59:10 am] ---
[0] [
[0]   {
[0]     age: 27306,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       openerURL: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       property: 'closed',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-to-coop-page-from-opener'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 29848,
[0]     body: {
[0]       columnNumber: 35,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       lineNumber: 91,
[0]       openerURL: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       property: 'closed',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       type: 'access-from-coop-page-to-opener'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:59:10 am] ---
[0] [
[0]   {
[0]     age: 544,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-plus-coep',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-plus-coep/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:59:10 am] ---
[0] [
[0]   {
[0]     age: 5173,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       openerURL: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       property: 'closed',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-to-coop-page-from-opener'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 9148,
[0]     body: {
[0]       columnNumber: 35,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       lineNumber: 91,
[0]       openerURL: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       property: 'closed',
[0]       referrer: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       type: 'access-from-coop-page-to-opener'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:59:10 am] ---
[0] [
[0]   {
[0]     age: 27306,
[0]     body: {
[0]       columnNumber: 28,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       lineNumber: 362,
[0]       openeeURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 29848,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       openeeURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 23173,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       lineNumber: 385,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 24849,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 31590,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       nextResponseURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 5173,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       lineNumber: 385,
[0]       openeeURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 9148,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'noopener-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       openeeURL: 'https://localhost:8443/ro-noopener-allow-popups/nav-test.html',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-noopener-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:59:10 am] ---
[0] [
[0]   {
[0]     age: 53826,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       openeeURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 46228,
[0]     body: {
[0]       columnNumber: 24,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       lineNumber: 378,
[0]       openeeURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       property: 'location',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 46210,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       type: 'access-to-coop-page-from-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 44548,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       lineNumber: 385,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 59391,
[0]     body: {
[0]       columnNumber: 47,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       initialPopupURL: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       lineNumber: 385,
[0]       openeeURL: '',
[0]       property: 'closed',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       type: 'access-from-coop-page-to-openee'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 40075,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       nextResponseURL: 'https://localhost:8443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]
[0]
[0] --- New Report Received [10:59:10 am] ---
[0] [
[0]   {
[0]     age: 46228,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       openerURL: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       property: 'location',
[0]       referrer: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       type: 'access-to-coop-page-from-opener'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 53826,
[0]     body: {
[0]       columnNumber: 35,
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       lineNumber: 91,
[0]       openerURL: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       property: 'closed',
[0]       referrer: 'https://localhost:8443/ro-same-origin-allow-popups/test.html',
[0]       sourceFile: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]       type: 'access-from-coop-page-to-opener'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   },
[0]   {
[0]     age: 46221,
[0]     body: {
[0]       disposition: 'reporting',
[0]       effectivePolicy: 'same-origin-allow-popups',
[0]       nextResponseURL: 'https://localhost:9443/',
[0]       type: 'navigation-from-response'
[0]     },
[0]     type: 'coop',
[0]     url: 'https://localhost:8443/ro-same-origin-allow-popups/nav-test.html',
[0]     user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
[0]   }
[0] ]

Replaces

https://github.com/mdn/content/pull/42639
https://github.com/mdn/content/pull/42051
-->

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- {{domxref("ReportingObserver")}}
- {{httpheader("Cross-Origin-Opener-Policy")}}
- {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}}
- {{HTTPHeader("Reporting-Endpoints")}}
- [Reporting API](/en-US/docs/Web/API/Reporting_API)
- [The Reporting API](https://developer.chrome.com/docs/capabilities/web-apis/reporting-api) (developer.chrome.com)
