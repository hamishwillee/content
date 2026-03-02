---
title: PermissionsPolicyViolationReport
slug: Web/API/PermissionsPolicyViolationReport
page-type: web-api-interface
browser-compat: api.ReportingObserver.ReportingObserver.options_parameter.types_property.permissions-policy-violation
spec-urls: https://w3c.github.io/webappsec-permissions-policy/#permissionspolicyviolationreportbody
---

{{APIRef("Reporting API")}}

The `PermissionsPolicyViolationReport` dictionary of the [Reporting API](/en-US/docs/Web/API/Reporting_API) represents a report that is generated when a document violates its {{httpheader("Permissions-Policy")}}.

Reports of this type can be observed from within a page using a {{domxref("ReportingObserver")}}, and a serialized version can be sent to a [reporting server endpoint](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints).

## Instance properties

- `body`
  - : The body of the report.
    This is an object with the following properties:
    - `featureId` {{experimental_inline}}
      - : A string representing the policy-controlled feature whose policy has been violated.
        This string can be used for grouping related reports.
    - `sourceFile` {{experimental_inline}}
      - : A string containing the path to the source file where the deprecated feature was used, if known, or `null` otherwise.
    - `lineNumber` {{experimental_inline}}
      - : A number representing the line in the source file in which the deprecated feature was used, if known, or `null` otherwise.
    - `columnNumber` {{experimental_inline}}
      - : A number representing the column in the source file in which the deprecated feature was first used, if known, or `null` otherwise.
    - `disposition`
      - : A string indicating whether the violation was enforced or only reported, corresponding to whether the policy was set with {{httpheader("Permissions-Policy")}} and {{httpheader("Permissions-Policy-Report-Only")}}, respectively.
        This can have the value `"enforce"` or `"reporting"`.
    - `allowAttribute` {{experimental_inline}}
      - : A string indicating the `allow` attribute of the specific {{htmlelement("iframe")}} in which the policy was violated, if relevant. Otherwise omitted.
    - `srcAttribute` {{experimental_inline}}
      - : A string indicating the `src` attribute of the specific {{htmlelement("iframe")}} in which the policy was violated, if relevant. Otherwise omitted.
- `type`
  - : The string `"permissions-policy-violation"` indicating that this is an `Permissions-Policy` violation report.
- `url`
  - : A string representing the URL of the document that generated the report.

## Description

Permissions Policy violations are reported when a document attempts to use a feature that is not allowed by it's policy, set using either the {{httpheader("Permissions-Policy")}} or {{httpheader("Permissions-Policy-Report-Only")}} HTTP headers.

<!--
Specifically, a report is sent when a document attempts to load a {{htmlelement("script")}} resource (or other [request destination](/en-US/docs/Web/API/Request/destination) listed in the policy) that does not have valid integrity metadata, or to make a request in [no-cors](/en-US/docs/Web/API/Request/mode#no-cors) mode. -->

You can monitor for violation reports within the page that sets the policy using the [Reporting API](/en-US/docs/Web/API/Reporting_API).
To do this you create a {{domxref("ReportingObserver")}} object to listen for reports, passing a callback method and an (optional) `options` property specifying the types of reports that you want to report on.
The callback method is then called with reports of the requested types, passing a report object.
For integrity violations, the object will be an `PermissionsPolicyViolationReport` instance (which has the [`type`](#type) property set to `"permissions-policy-violation"`).

The structure of a typical report is shown below.
Note that we can see the URL of both the page that had its policy violated (`url`), the file location where the feature usage was attempted (`body.sourceFile`, `body.lineNumber`, `body.columnNumber`), and the feature identifier (`body.featureId`).
We can also see that the report was triggered by a violation that was enforced (and not just reported) and a message with more detail.

```json
{
  "type": "permissions-policy-violation",
  "url": "https://url-of-page-setting-violated-permissions-policy",
  "body": {
    "sourceFile": "https://example.com/",
    "lineNumber": 44,
    "columnNumber": 29,
    "featureId": "geolocation",
    "disposition": "enforce",
    "message": "Permissions policy violation: Geolocation access has been blocked because of a permissions policy applied to the current document. See https://crbug.com/414348233 for more details."
  }
}
```

<!--  Below needs testing
Caddyfile has default endpoint - check that works.
Spec says Member Values may have a Parameter named "report-to", whose value must be a String. Any other parameters will be ignored.
SHould check how that might work exactly. I read that as one endpoin tfor each check - see
Permissions-Policy: camera=();report-to="security-endpoint", geolocation=();report-to="security-endpoint".
-->

Violation reports may also sent as a JSON object in a `POST` to one or more configured [reporting server endpoints](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints).
Reporting server endpoint names are specified in the [`endpoints` list](/en-US/docs/Web/HTTP/Reference/Headers/Integrity-Policy#endpoints) when setting {{httpheader("Integrity-Policy")}} or {{httpheader("Integrity-Policy-Report-Only")}}.
Valid endpoint names and their mapping to a particular URL are defined using the {{httpheader("Reporting-Endpoints")}} header.

The structure of the server report is almost exactly the same as `PermissionsPolicyViolationReport`, except that it additionally includes `age` and `user_agent` fields.

```json
{
  "age": "176279",
  "body": {
    "sourceFile": "https://example.com/",
    "lineNumber": 44,
    "columnNumber": 29,
    "featureId": "geolocation",
    "disposition": "enforce",
    "message": "Permissions policy violation: Geolocation access has been blocked because of a permissions policy applied to the current document. See https://crbug.com/414348233 for more details."
  },
  "type": "permissions-policy-violation",
  "url": "https://url-of-page-setting-violated-permissions-policy",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}
```

## Examples

### Using the `ReportingObserver` interface

<!--

Code that works

    </style>
    <meta http-equiv="Permissions-Policy" content="geolocation=()">
  </head>

  <body>
    <h1>Reporting API: permissions-policy-violation Test Page</h1>
    <p>Status: Check the box below and the console for violation reports.</p>
    <hr />
    <div id="report-display">Waiting for reports...</div>
    <hr />

    <script>
      const display = document.getElementById("report-display");

      const options = {
        types: ["permissions-policy-violation"],
        buffered: true,
      };

      const observer = new ReportingObserver((reports, observer) => {
        const firstReport = reports[0];
        display.innerText = JSON.stringify(firstReport, null, 2);
        console.log(firstReport);
      }, options);

      // 2. Start observing
      observer.observe();

      //3. Trigger intervention report by doing forbidden task
      navigator.geolocation.getCurrentPosition(
        () => {},
        () => {},
      );
    </script>
  </body>
</html>

-->

This example shows how you can obtain Integrity Policy violation reports using a {{domxref("ReportingObserver")}}.

First we set a page's integrity policy using the {{httpheader("Integrity-Policy")}}.
The policy below reports and blocks resource loading of any {{htmlelement("script")}} element or {{domxref("HTMLScriptElement")}} object that does not specify an `integrity` attribute, or when a script resource is requested in [no-cors](/en-US/docs/Web/API/Request/mode#no-cors) mode.
Note that for this example we're only interested in reporting the violations using the API, so we're omitting the reporting endpoints:

```http
Integrity-Policy: blocked-destinations=(script)
```

Next, we'll assume that our page includes the following element to load a script.
Because we want to trigger a violation, it omits the `integrity` attribute used to check the script matches our expected version.
We could also omit the `cross-origin` attribute so the request is sent in `no-cors` mode.

```html
<script
  src="https://example.com/example-framework.js"
  crossorigin="anonymous"></script>
```

> [!NOTE]
> A script that complies with the policy might look like this:
>
> ```html
> <script
>   src="https://example.com/example-framework.js"
>   integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
>   crossorigin="anonymous"></script>
> ```

To observe violations within the page, we construct a new {{domxref("ReportingObserver")}} object to listen for reports with the type `"integrity-violation"`, passing a callback that will receive and log the reports.
This code needs to be loaded before the script that causes the violation, in the same page:

```js
const observer = new ReportingObserver(
  (reports, observer) => {
    reports.forEach((violation) => {
      console.log(violation);
      console.log(JSON.stringify(violation));
    });
  },
  {
    types: ["permissions-policy-violation"],
    buffered: true,
  },
);

observer.observe();
```

Above, we log each violation report object and a JSON-string version of the object, which might look similar to the object below.

```json
{
  "type": "permissions-policy-violation",
  "url": "https://example.com",
  "body": {
    "documentURL": "https://example.com",
    "blockedURL": "https://example.com/example-framework.js",
    "destination": "script",
    "reportOnly": false
  }
}
```

### Sending a report to a reporting endpoint

Configuring a web page to send an Integrity Policy violation report to a [reporting server endpoint](/en-US/docs/Web/API/Reporting_API#reporting_server_endpoints) is very similar to the previous example.

The main difference is that we need to specify one or more reporting endpoints where we want the reports to be sent, using the {{httpheader("Reporting-Endpoints")}} response header, and then reference these in the `endpoints` field when setting the policy.

You can see this below, where we first define two endpoints — `integrity-endpoint` and `backup-integrity-endpoint` — and then reference them in our policy:

```http
Reporting-Endpoints: integrity-endpoint=https://example.com/integrity, backup-integrity-endpoint=https://report-provider.example/integrity
Integrity-Policy: blocked-destinations=(script), endpoints=(integrity-endpoint, backup-integrity-endpoint)
```

We can trigger a violation by loading an external script from the page that does not meet the subresource integrity guidelines.
Just to differ from the previous example, here we send the request in `no-cors` mode:

```html
<script
  src="https://example.com/example-framework.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"></script>
```

The violation report will then be sent to the indicated endpoint as a JSON file.
As you can see from the example below, the `type` is `"integrity-violation"` and the `body` property is a serialization of this `IntegrityViolationReport` object:

The report in this case would look the same as our JSON report in the previous example.

```json
{
  "type": "integrity-violation",
  "url": "https://example.com",
  "body": {
    "documentURL": "https://example.com",
    "blockedURL": "https://example.com/example-framework.js",
    "destination": "script",
    "reportOnly": false
  }
}
```

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- {{domxref("ReportingObserver")}}
- {{HTTPHeader("Integrity-Policy")}}
- {{HTTPHeader("Integrity-Policy-Report-Only")}}
- {{HTTPHeader("Reporting-Endpoints")}}
- [Integrity Policy](/en-US/docs/Web/Security/Defenses/Subresource_Integrity#integrity_policy) in [Subresource Integrity](/en-US/docs/Web/Security/Defenses/Subresource_Integrity#integrity_policy)
- [Reporting API](/en-US/docs/Web/API/Reporting_API)
