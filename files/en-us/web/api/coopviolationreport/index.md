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

The `COOPViolationReport` dictionary of the [Reporting API](/en-US/docs/Web/API/Reporting_API) represents a report generated when a document violates its {{httpheader("Cross-Origin-Opener-Policy")}} (COOP).

Reports of this type can be observed from within a page using a {{domxref("ReportingObserver")}}, or a serialized version can be sent to a [reporting server endpoint](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints).

<!-- note, not all of them - " COOP property access reports are also visible to reporting observers. The navigation ones are not. " -->

## Instance properties

- `body`
  - : The body of the report.
    This is an object with the following properties:
    - `type`
      - : A string representing the cause of the violation that triggered the report.
        This property is present in every report.
        It can have one of the following values:
        - [`access-to-opener`] , Fired when a page accesses a property on its cross-origin opener window. Visible to ReportingObserver.
        - [`access-to-opened-window`] , Fired when a page accesses a property on a cross-origin window it opened. Visible to ReportingObserver.
        - [`navigation-from-response`](#navigation-from-response_report), Fired on the page being navigated away from when the new document has an incompatible COOP.
        - [`navigation-to-response`](#navigation-from-response_report) Fred on the page being navigated to when the incoming document has an incompatible COOP.

        <!--
        // https://html.spec.whatwg.org/multipage/browsers.html#coop-violation-navigation-to
        // https://html.spec.whatwg.org/multipage/browsers.html#coop-violation-navigation-from
        // https://html.spec.whatwg.org/multipage/browsers.html#coop-violation-access-to-opener
        //https://html.spec.whatwg.org/multipage/browsers.html#coop-violation-access-from-opened
        /// https://html.spec.whatwg.org/multipage/browsers.html#coop-violation-access-to-opened
        There might be more
        -->

    - `disposition`
      - : A string indicating whether the violation was enforced or only reported.
        This property is present in every report.
        It can have one of the following values:
        - `"enforce"`
          - : The violation caused opening of the resource to be blocked.
            This is set for violations of policies set with {{httpheader("Cross-Origin-Opener-Policy")}}.
        - `"reporting"`
          - : The violation was reported without blocking the resource from opening.
            This is set for violations of policies set with {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}}.
    - `effectivePolicy`
      - : A string indicating the effective COOP policy of the document for which the violation report is being sent.
        This property is present in every report.
        Whether the policy is enforced or only reported against depends on the [`disposition`](#disposition).

        This is the COOP policy value triggered the violation. Possible values: `"unsafe-none"`, `"same-origin"`, `"same-origin-allow-popups"`, `"same-origin-plus-COEP"`, `"noopener-allow-popups"`. <!-- check -->

    - `previousResponseURL`
      - : A string indicating the sanitized URL of the opener of a document.
        This is reported for an opened document in a report with a [`body.type`](#type) of [`navigation-to-response`](#navigation-to-response_report).
    - `nextResponseURL`
      - : A string indicating the sanitized URL of the opened document.
        This is reported for an opener document in a report with a [`body.type`](#type) of [`navigation-from-response`](#navigation-from-response_report).
    - `referrer`
      - : A string representing Xxxxxx
        This is reported for an opener <!-- check --> document in a report with a [`body.type`](#type) of [`navigation-to-response`](#navigation-to-response) or [`access-to-opener`]().
    - `property`
      - : A string representing whether XXXX
        This is reported for an opener <!-- check --> document in a report with a [`body.type`](#type) of [access-to-opened-window`](#access-to-opened-window) or [`access-to-opener`]().
    - `openerURL`
      - : A string representing whether XXXX
        [`access-to-opener`](#access-to-opener)
    - `openedWindowURL`
      - : A string representing whether XXXX
        [`access-to-opened-window`](#access-to-opened-window)
    - `openedWindowInitialURL`
      - : A string representing whether XXXX
        [`access-to-opened-window`](#access-to-opened-window)
    - `sourceFile`
      - : A string indicating the URL of the script that triggered the violation report.
        [`access-to-opener`](#access-to-opener), [`access-to-opened-window`](#access-to-opened-window)
    - `lineNumber`
      - : A string indicating the line number in the script that triggered the violation report.
        [`access-to-opener`](#access-to-opener), [`access-to-opened-window`](#access-to-opened-window)
    - `columnNumber`
      - : A string indicating the column number in the script that triggered the violation report.
        [`access-to-opener`](#access-to-opener), [`access-to-opened-window`](#access-to-opened-window)

  - : The string `"coop"`, indicating that this is a COOP violation report.

- `url`
  - : A string representing the URL of the document that generated the report.

<!--- BELOW HERE ALL UNDER CONSTRUCTION - some is mined from other docs - some of it is original coep -->

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

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- {{domxref("ReportingObserver")}}
- {{httpheader("Cross-Origin-Embedder-Policy")}}
- {{httpheader("Cross-Origin-Embedder-Policy-Report-Only")}}
- {{HTTPHeader("Reporting-Endpoints")}}
- [Reporting API](/en-US/docs/Web/API/Reporting_API)
- [The Reporting API](https://developer.chrome.com/docs/capabilities/web-apis/reporting-api) (developer.chrome.com)

<!-- BELOW HERE IS THE NEW DOC WE WANT TO INTEGRATE -->
<!--

## Description
When navigating to a new document, or using {{domxref("window.open()")}} to open a document, the new document may be opened in the same {{glossary("Browsing context","browsing context group (BCG)")}} as the original document, or in a new BCG.
If a document is opened in a new BCG it is [cross-origin isolated](/en-US/docs/Web/API/Window/crossOriginIsolated) from the original document, which closes a number of paths for malicious code.

Document policies can be set and enforced using the {{httpheader("Cross-Origin-Opener-Policy")}} HTTP header, or set and reported-on (but not enforced) using the {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}} header.

COOP policy violations may be reported using the [Reporting API](/en-US/docs/Web/API/Reporting_API) whenever a policy causes (or would cause) a document to be opened in a new BCG, or if the opened document attempts to access its opener.

A COOP policy violation report is represented by a {{domxref("Report")}} instance that has the {{domxref("Report.type","type")}} of `coop` and a {{domxref("Report.body","body")}} property that is an object of this type.
Reports can be returned via the {{domxref("ReportingObserver")}} interface or serialized and sent in a `POST` to a [reporting server endpoint](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints).

To send to a reporting server endpoint the {{httpheader("Cross-Origin-Opener-Policy")}} and/or {{httpheader("Cross-Origin-Opener-Policy-Report-Only")}} headers used to set the policy must include the `report-to` parameter with a valid reporting endpoint name.
Valid endpoint names are defined using the {{httpheader("Reporting-Endpoints")}} header.

### Reporting enforcement and report-only policy violations

The `Cross-Origin-Opener-Policy` header is used to enforce a COOP policy for a particular document.
The policy effectively defines the policy(s) that other documents must have in order to open or navigate to the document in the same BCG, and in order to be opened or navigated from this document and remain in the same BCG.

The `Cross-Origin-Opener-Policy-Report-Only` can be used to test the effect of enforcing a COOP policy for a particular document.
When the document opens or is opened by another document its reporting-only policy is compared to the actual policy of the other document to determine if there would be a violation and send an appropriate report.

A document can set `Cross-Origin-Opener-Policy` and/or `Cross-Origin-Opener-Policy-Report-Only` headers.
These can have the same or different policies and reporting endpoints.
-->

### Types of reports

Different reports are sent depending on whether the reporter is the opener or opened document in a navigation, or if the report is for a COOP access violation.
The types of these reports is indicated by the [`body.type](#type) property (the {{domxref("Report.type")}} is`coep` for all of these).

#### `navigation-to-response` report

<!-- navigation-to-response - Fired on the page being navigated to when the incoming document has an incompatible COOP. -->

This type of report is sent to the COOP reporting endpoint, if specified, of a document that is navigated-to (pened) in a navigation.

For an enforced COOP policy, it indicates that the document was opened in a new BCG.
This occurs when the COOP policy of the opened document is incompatible with that of its opener.
For navigations this means that the opened document has a different COOP policy from its opener, or the same policy but they are not same-site (unless both documents have a COOP policy of [`unsafe-none`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy#unsafe-none)).

For a report-only COOP policy, it indicates the report-only COOP policy is incompatible with the (enforced) policy of its opener.
In other words, that the report-only policy set in `Cross-Origin-Opener-Policy-Report-Only` would result in a violation if it was enforced.

The report has the following body properties:

- `type`: `navigation-to-response`
- `disposition`: Whether the report is for an `enforced` or `reporting` policy.
- `effectivePolicy`: The effective policy of the opened document.
  This policy may be an enforced or reporting-only policy, depending on the [`disposition`](#disposition).

- `previousResponseURL`: The sanitized URL of the previous document (that was navigated from), or `null` for cross-origin navigations.
  This is the URL of the opener.
  It might be the same URL as the {{domxref("COOPViolationReportBody.referrer","referrer")}} or it might be an intermediate redirect URL.
- `referrer`: The original URL that started the navigation chain that resulted in this report.

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
  This may be an enforced or reporting-only policy, depending on the {{domxref("COOPViolationReportBody.disposition","disposition")}}.

- [`nextResponseURL`](#nextresponseurl): The sanitized URL of the opened document (that was navigated to), or `null` for cross origin navigations.

#### `access-to-opener` report

  <!-- access-to-opener:   Fired when a page accesses a property on its cross-origin opener window. Visible to ReportingObserver. -->

- disposition
- effectivePolicy
- type

- property
- openerURL

sourceFile
lineNumber
columnNumber

TE THIS IS MORE COMPLICATED - there are two possible reports. Have not yet worked out why need both

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

-->

#### `access-to-opened-window` report

<!-- access-to-opened-window:   Fired when a page accesses a property on a cross-origin window it opened. Visible to ReportingObserver. -->

- disposition
- effectivePolicy
- type

- property
- openedWindowInitialURL
- sourceFile
- columnNumber

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

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- {{httpheader("Reporting-Endpoints")}}
- [Reporting API](/en-US/docs/Web/API/Reporting_API)
- [The Reporting API](https://developer.chrome.com/docs/capabilities/web-apis/reporting-api)

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

Replaces

https://github.com/mdn/content/pull/42639
https://github.com/mdn/content/pull/42051
-->
