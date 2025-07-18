---
title: "<link>: The External Resource Link element"
slug: Web/HTML/Reference/Elements/link
page-type: html-element
browser-compat: html.elements.link
sidebar: htmlsidebar
---

The **`<link>`** [HTML](/en-US/docs/Web/HTML) element specifies relationships between the current document and an external resource.
This element is most commonly used to link to {{Glossary("CSS", "stylesheets")}}, but is also used to establish site icons (both "favicon" style icons and icons for the home screen and apps on mobile devices) among other things.

{{InteractiveExample("HTML Demo: &lt;link&gt;", "tabbed-shorter")}}

```html interactive-example
<link href="/shared-assets/misc/link-element-example.css" rel="stylesheet" />

<p>This text will be red as defined in the external stylesheet.</p>
<p style="color: blue">
  The <code>style</code> attribute can override it, though.
</p>
```

To link an external stylesheet, you'd include a `<link>` element inside your {{HTMLElement("head")}} like this:

```html
<link href="main.css" rel="stylesheet" />
```

This example provides the path to the stylesheet inside an `href` attribute and a [`rel`](/en-US/docs/Web/HTML/Reference/Attributes/rel) attribute with a value of `stylesheet`. The `rel` stands for "relationship", and is one of the key features of the `<link>` element — the value denotes how the item being linked to is related to the containing document.

There are a number of other common types you'll come across. For example, a link to the site's favicon:

```html
<link rel="icon" href="favicon.ico" />
```

There are a number of other icon `rel` values, mainly used to indicate special icon types for use on various mobile platforms, e.g.:

```html
<link
  rel="apple-touch-icon"
  sizes="114x114"
  href="apple-icon-114.png"
  type="image/png" />
```

The `sizes` attribute indicates the icon size, while the `type` contains the MIME type of the resource being linked.
These provide useful hints to allow the browser to choose the most appropriate icon available.

You can also provide a media type or query inside a `media` attribute; this resource will then only be loaded if the media condition is true. For example:

```html
<link href="print.css" rel="stylesheet" media="print" />
<link href="mobile.css" rel="stylesheet" media="screen and (width <= 600px)" />
```

Some interesting new performance and security features have been added to the `<link>` element too. Take this example:

```html
<link
  rel="preload"
  href="myFont.woff2"
  as="font"
  type="font/woff2"
  crossorigin="anonymous" />
```

A `rel` value of `preload` indicates that the browser should preload this resource (see [`rel="preload"`](/en-US/docs/Web/HTML/Reference/Attributes/rel/preload) for more details), with the `as` attribute indicating the specific class of content being fetched.
The `crossorigin` attribute indicates whether the resource should be fetched with a {{Glossary("CORS")}} request.

Other usage notes:

- A `<link>` element can occur either in the {{HTMLElement("head")}} or {{HTMLElement("body")}} element, depending on whether it has a [link type](https://html.spec.whatwg.org/multipage/links.html#body-ok) that is **body-ok**.
  For example, the `stylesheet` link type is body-ok, and therefore `<link rel="stylesheet">` is permitted in the body.
  However, this isn't a good practice to follow; it makes more sense to separate your `<link>` elements from your body content, putting them in the `<head>`.
- When using `<link>` to establish a favicon for a site, and your site uses a Content Security Policy (CSP) to enhance its security, the policy applies to the favicon.
  If you encounter problems with the favicon not loading, verify that the {{HTTPHeader("Content-Security-Policy")}} header's [`img-src` directive](/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/img-src) is not preventing access to it.
- The HTML and XHTML specifications define event handlers for the `<link>` element, but it is unclear how they would be used.
- Under XHTML 1.0, {{glossary("void element", "void elements")}} such as `<link>` require a trailing slash: `<link />`.
- WebTV supports the use of the value `next` for `rel` to preload the next page in a document series.

## Attributes

This element includes the [global attributes](/en-US/docs/Web/HTML/Reference/Global_attributes).

- `as`
  - : This attribute is required when [`rel="preload"`](/en-US/docs/Web/HTML/Reference/Attributes/rel/preload) has been set on the `<link>` element, optional when [`rel="modulepreload"`](/en-US/docs/Web/HTML/Reference/Attributes/rel/modulepreload) has been set, and otherwise should not be used.
    It specifies the type of content being loaded by the `<link>`, which is necessary for request matching, application of correct [content security policy](/en-US/docs/Web/HTTP/Guides/CSP), and setting of correct {{HTTPHeader("Accept")}} request header.

    Furthermore, `rel="preload"` uses this as a signal for request prioritization.
    The table below lists the valid values for this attribute and the elements or resources they apply to.

    <table class="standard-table">
      <thead>
        <tr>
          <th scope="col">Value</th>
          <th scope="col">Applies To</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>audio</td>
          <td><code>&#x3C;audio></code> elements</td>
        </tr>
        <tr>
          <td>document</td>
          <td><code>&#x3C;iframe></code> and <code>&#x3C;frame></code> elements</td>
        </tr>
        <tr>
          <td>embed</td>
          <td><code>&#x3C;embed></code> elements</td>
        </tr>
        <tr>
          <td>fetch</td>
          <td>
            <p>fetch, XHR</p>
            <div class="notecard note">
              <p>
                <strong>Note:</strong> This value also requires
                <code>&#x3C;link></code> to contain the crossorigin attribute, see <a href="/en-US/docs/Web/HTML/Reference/Attributes/rel/preload#cors-enabled_fetches">CORS-enabled fetches</a>.
              </p>
            </div>
          </td>
        </tr>
        <tr>
          <td>font</td>
          <td>
            <p>CSS @font-face</p>
            <div class="notecard note">
              <p>
                <strong>Note:</strong> This value also requires
                <code>&#x3C;link></code> to contain the crossorigin attribute, see <a href="/en-US/docs/Web/HTML/Reference/Attributes/rel/preload#cors-enabled_fetches">CORS-enabled fetches</a>.
              </p>
            </div>
          </td>
        </tr>
        <tr>
          <td>image</td>
          <td>
            <code>&#x3C;img></code> and <code>&#x3C;picture></code> elements with
            srcset or imageset attributes, SVG <code>&#x3C;image></code> elements,
            CSS <code>*-image</code> rules
          </td>
        </tr>
        <tr>
          <td>object</td>
          <td><code>&#x3C;object></code> elements</td>
        </tr>
        <tr>
          <td>script</td>
          <td>
            <code>&#x3C;script></code> elements, Worker <code>importScripts</code>
          </td>
        </tr>
        <tr>
          <td>style</td>
          <td>
            <code>&#x3C;link rel=stylesheet></code> elements, CSS
            <code>@import</code>
          </td>
        </tr>
        <tr>
          <td>track</td>
          <td><code>&#x3C;track></code> elements</td>
        </tr>
        <tr>
          <td>video</td>
          <td><code>&#x3C;video></code> elements</td>
        </tr>
        <tr>
          <td>worker</td>
          <td>Worker, SharedWorker</td>
        </tr>
      </tbody>
    </table>

- `blocking`
  - : This attribute explicitly indicates that certain operations should be blocked on the fetching of an external resource. It must only be used when the `rel` attribute contains `expect` or `stylesheet` keywords. The operations that are to be blocked must be a space-separated list of blocking tokens listed below.
    - `render`: The rendering of content on the screen is blocked.

- [`crossorigin`](/en-US/docs/Web/HTML/Reference/Attributes/crossorigin)
  - : This [enumerated](/en-US/docs/Glossary/Enumerated) attribute indicates whether {{Glossary("CORS")}} must be used when fetching the resource.
    [CORS-enabled images](/en-US/docs/Web/HTML/How_to/CORS_enabled_image) can be reused in the {{HTMLElement("canvas")}} element without being _tainted_.
    The allowed values are:
    - `anonymous`
      - : A cross-origin request (i.e., with an {{HTTPHeader("Origin")}} HTTP header) is performed, but no credential is sent (i.e., no cookie, X.509 certificate, or HTTP Basic authentication).
        If the server does not give credentials to the origin site (by not setting the {{HTTPHeader("Access-Control-Allow-Origin")}} HTTP header) the resource will be tainted and its usage restricted.
    - `use-credentials`
      - : A cross-origin request (i.e., with an `Origin` HTTP header) is performed along with a credential sent (i.e., a cookie, certificate, and/or HTTP Basic authentication is performed).
        If the server does not give credentials to the origin site (through {{HTTPHeader("Access-Control-Allow-Credentials")}} HTTP header), the resource will be _tainted_ and its usage restricted.

    If the attribute is not present, the resource is fetched without a {{Glossary("CORS")}} request (i.e., without sending the `Origin` HTTP header), preventing its non-tainted usage. If invalid, it is handled as if the enumerated keyword **anonymous** was used.
    See [CORS settings attributes](/en-US/docs/Web/HTML/Reference/Attributes/crossorigin) for additional information.

- `disabled`
  - : For `rel="stylesheet"` only, the `disabled` Boolean attribute indicates whether the described stylesheet should be loaded and applied to the document.
    If `disabled` is specified in the HTML when it is loaded, the stylesheet will not be loaded during page load.
    Instead, the stylesheet will be loaded on-demand, if and when the `disabled` attribute is changed to `false` or removed.

    Setting the `disabled` property in the DOM causes the stylesheet to be removed from the document's {{domxref("Document.styleSheets")}} list.

- `fetchpriority`
  - : Provides a hint of the relative priority to use when fetching a resource of a particular type.
    Allowed values:
    - `high`
      - : Fetch the resource at a high priority relative to other resources of the same type.
    - `low`
      - : Fetch the resource at a low priority relative to other resources of the same type.
    - `auto`
      - : Don't set a preference for the fetch priority.
        This is the default.
        It is used if no value or an invalid value is set.

    See {{domxref("HTMLLinkElement.fetchPriority")}} for more information.

- `href`
  - : This attribute specifies the {{glossary("URL")}} of the linked resource. A URL can be absolute or relative.
- `hreflang`
  - : This attribute indicates the language of the linked resource.
    It is purely advisory.
    Allowed values are specified by {{RFC(5646, "Tags for Identifying Languages (also known as BCP 47)")}}.
    Use this attribute only if the [`href`](/en-US/docs/Web/HTML/Reference/Elements/a#href) attribute is present.
- `imagesizes`
  - : For `rel="preload"` and `as="image"` only, the `imagesizes` attribute has similar syntax and semantics as the [`sizes`](/en-US/docs/Web/HTML/Reference/Elements/img#sizes) attribute that indicates to preload the appropriate resource used by an `img` element with corresponding values for its `srcset` and `sizes` attributes.
- `imagesrcset`
  - : For `rel="preload"` and `as="image"` only, the `imagesrcset` attribute has similar syntax and semantics as the [`srcset`](/en-US/docs/Web/HTML/Reference/Elements/img#srcset) attribute that indicates to preload the appropriate resource used by an `img` element with corresponding values for its `srcset` and `sizes` attributes.
- `integrity`
  - : Contains inline metadata — a base64-encoded cryptographic hash of the resource (file) you're telling the browser to fetch.
    The browser can use this to verify that the fetched resource has been delivered without unexpected manipulation.
    The attribute must only be specified when the `rel` attribute is specified to `stylesheet`, `preload`, or `modulepreload`.
    See [Subresource Integrity](/en-US/docs/Web/Security/Subresource_Integrity).
- `media`
  - : This attribute specifies the media that the linked resource applies to. Its value must be a media type / [media query](/en-US/docs/Web/CSS/CSS_media_queries).
    This attribute is mainly useful when linking to external stylesheets — it allows the user agent to pick the best adapted one for the device it runs on.

- `referrerpolicy`
  - : A string indicating which referrer to use when fetching the resource:
    - `no-referrer` means that the {{HTTPHeader("Referer")}} header will not be sent.
    - `no-referrer-when-downgrade` means that no {{HTTPHeader("Referer")}} header will be sent when navigating to an origin without TLS (HTTPS).
      This is a user agent's default behavior, if no policy is otherwise specified.
    - `origin` means that the referrer will be the origin of the page, which is roughly the scheme, the host, and the port.
    - `origin-when-cross-origin` means that navigating to other origins will be limited to the scheme, the host, and the port, while navigating on the same origin will include the referrer's path.
    - `unsafe-url` means that the referrer will include the origin and the path (but not the fragment, password, or username).
      This case is unsafe because it can leak origins and paths from TLS-protected resources to insecure origins.

- [`rel`](/en-US/docs/Web/HTML/Reference/Attributes/rel)
  - : This attribute names a relationship of the linked document to the current document. The attribute must be a space-separated list of [link type values](/en-US/docs/Web/HTML/Reference/Attributes/rel).
- `sizes`
  - : This attribute defines the sizes of the icons for visual media contained in the resource.
    It must be present only if the [`rel`](#rel) contains a value of `icon` or a non-standard type such as Apple's `apple-touch-icon`.
    It may have the following values:
    - `any`, meaning that the icon can be scaled to any size as it is in a vector format, like `image/svg+xml`.
    - a white-space separated list of sizes, each in the format `<width in pixels>x<height in pixels>` or `<width in pixels>X<height in pixels>`. Each of these sizes must be contained in the resource.

    > [!NOTE]
    > Most icon formats are only able to store one single icon; therefore, most of the time, the [`sizes`](#sizes) attribute contains only one entry.
    > Microsoft's ICO format and Apple's ICNS format can store multiple icon sizes in a single file. ICO has better browser support, so you should use this format if cross-browser support is a concern.

- `title`
  - : The `title` attribute has special semantics on the `<link>` element.
    When used on a `<link rel="stylesheet">` it defines a [default or an alternate stylesheet](/en-US/docs/Web/HTML/Reference/Attributes/rel/alternate_stylesheet).
- `type`
  - : This attribute is used to define the type of the content linked to.
    The value of the attribute should be a MIME type such as **text/html**, **text/css**, and so on.
    The common use of this attribute is to define the type of stylesheet being referenced (such as **text/css**), but given that CSS is the only stylesheet language used on the web, not only is it possible to omit the `type` attribute, but is actually now recommended practice.
    It is also used on `rel="preload"` link types, to make sure the browser only downloads file types that it supports.

### Non-standard attributes

- `target` {{Deprecated_Inline}}
  - : Defines the frame or window name that has the defined linking relationship or that will show the rendering of any linked resource.

### Obsolete attributes

- `charset` {{deprecated_inline}}
  - : This attribute defines the character encoding of the linked resource.
    The value is a space- and/or comma-delimited list of character sets as defined in {{rfc(2045)}}.
    The default value is `iso-8859-1`.

    > [!NOTE]
    > To produce the same effect as this obsolete attribute, use the {{HTTPHeader("Content-Type")}} HTTP header on the linked resource.

- `rev` {{deprecated_inline}}
  - : The value of this attribute shows the relationship of the current document to the linked document, as defined by the [`href`](#href) attribute.
    The attribute thus defines the reverse relationship compared to the value of the `rel` attribute.
    [Link type values](/en-US/docs/Web/HTML/Reference/Attributes/rel) for the attribute are similar to the possible values for [`rel`](#rel).

    > [!NOTE]
    > Instead of `rev`, you should use the [`rel`](#rel) attribute with the opposite [link type value](/en-US/docs/Web/HTML/Reference/Attributes/rel).
    > For example, to establish the reverse link for `made`, specify `author`. Also, this attribute doesn't stand for "revision" and must not be used with a version number, even though many sites misuse it in this way.

## Examples

### Including a stylesheet

To include a stylesheet in a page, use the following syntax:

```html
<link href="style.css" rel="stylesheet" />
```

### Providing alternative stylesheets

You can also specify [alternative style sheets](/en-US/docs/Web/HTML/Reference/Attributes/rel/alternate_stylesheet).

The user can choose which style sheet to use by choosing it from the **View > Page Style** menu.
This provides a way for users to see multiple versions of a page.

```html
<link href="default.css" rel="stylesheet" title="Default Style" />
<link href="fancy.css" rel="alternate stylesheet" title="Fancy" />
<link href="basic.css" rel="alternate stylesheet" title="Basic" />
```

### Providing icons for different usage contexts

You can include links to several icons on the same page, and the browser will choose which one works best for its particular context using the `rel` and `sizes` values as hints.

```html
<!-- iPad Pro with high-resolution Retina display: -->
<link
  rel="apple-touch-icon"
  sizes="167x167"
  href="/apple-touch-icon-167x167.png" />
<!-- 3x resolution iPhone: -->
<link
  rel="apple-touch-icon"
  sizes="180x180"
  href="/apple-touch-icon-180x180.png" />
<!-- non-Retina iPad, iPad mini, etc.: -->
<link
  rel="apple-touch-icon"
  sizes="152x152"
  href="/apple-touch-icon-152x152.png" />
<!-- 2x resolution iPhone and other devices: -->
<link rel="apple-touch-icon" href="/apple-touch-icon-120x120.png" />
<!-- basic favicon -->
<link rel="icon" href="/favicon.ico" />
```

For information about what `sizes` to choose for Apple icons, see [Apple's documentation on configuring web applications](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html#//apple_ref/doc/uid/TP40002051-CH3-SW4) and the referenced [Apple human interface guidelines](https://developer.apple.com/design/human-interface-guidelines/app-icons#App-icon-sizes). Usually, it is sufficient to provide a large image, such as 192x192, and let the browser scale it down as needed, but you may want to provide images with different levels of detail for different sizes, as the Apple design guideline recommends. Providing smaller icons for lower resolutions also saves bandwidth.

It may not be necessary to provide `<link>` elements at all. For example, browsers automatically request `/favicon.ico` from the root of a site, and Apple also automatically requests `/apple-touch-icon-[size].png`, `/apple-touch-icon.png`, etc. However, providing explicit links protects you against changes to these conventions.

### Conditionally loading resources with media queries

You can provide a media type or query inside a `media` attribute;
this resource will then only be loaded if the media condition is true. For example:

```html
<link href="print.css" rel="stylesheet" media="print" />
<link href="mobile.css" rel="stylesheet" media="all" />
<link href="desktop.css" rel="stylesheet" media="screen and (width >= 600px)" />
<link
  href="highres.css"
  rel="stylesheet"
  media="screen and (resolution >= 300dpi)" />
```

### Stylesheet load events

You can determine when a style sheet has been loaded by watching for a `load` event to fire on it; similarly, you can detect if an error has occurred while processing a style sheet by watching for an `error` event:

```html
<link rel="stylesheet" href="mystylesheet.css" id="my-stylesheet" />
```

```js
const stylesheet = document.getElementById("my-stylesheet");

stylesheet.onload = () => {
  // Do something interesting; the sheet has been loaded
};

stylesheet.onerror = () => {
  console.log("An error occurred loading the stylesheet!");
};
```

> [!NOTE]
> The `load` event fires once the stylesheet and all of its imported content has been loaded and parsed, and immediately before the styles start being applied to the content.

### Preload examples

You can find a number of `<link rel="preload">` examples in [Preloading content with `rel="preload"`](/en-US/docs/Web/HTML/Reference/Attributes/rel/preload).

### Blocking rendering till a resource is fetched

You can include `render` token inside a `blocking` attribute;
the rendering of the page will be blocked till the resource is fetched. For example:

```html
<link blocking="render" rel="stylesheet" href="example.css" crossorigin />
```

## Technical summary

<table class="properties">
  <tbody>
    <tr>
      <th>
        <a href="/en-US/docs/Web/HTML/Guides/Content_categories">Content categories</a>
      </th>
      <td>
        Metadata content.
        If <code><a href="/en-US/docs/Web/HTML/Reference/Global_attributes/itemprop">itemprop</a></code> is present:
        <a href="/en-US/docs/Web/HTML/Guides/Content_categories#flow_content">Flow content</a> and
        <a href="/en-US/docs/Web/HTML/Guides/Content_categories#phrasing_content">phrasing content</a>.
      </td>
    </tr>
    <tr>
      <th>Permitted content</th>
      <td>None; it is a {{Glossary("void element")}}.</td>
    </tr>
    <tr>
      <th>Tag omission</th>
      <td>Must have a start tag and must not have an end tag.</td>
    </tr>
    <tr>
      <th>Permitted parents</th>
      <td>
        Any element that accepts metadata elements.
        If <a href="/en-US/docs/Web/HTML/Reference/Global_attributes/itemprop">itemprop</a> is present: any element that accepts
        <a href="/en-US/docs/Web/HTML/Guides/Content_categories#phrasing_content">phrasing content</a>.
      </td>
    </tr>
    <tr>
      <th scope="row">Implicit ARIA role</th>
      <td><a href="/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/link_role"><code>link</code></a> with <code>href</code> attribute</td>
    </tr>
    <tr>
      <th scope="row">Permitted ARIA roles</th>
      <td>No <code>role</code> permitted</td>
    </tr>
    <tr>
      <th>DOM interface</th>
      <td>{{DOMxRef("HTMLLinkElement")}}</td>
    </tr>
  </tbody>
</table>

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- {{HTTPHeader("Link")}} HTTP header
