---
title: Firefox 125 for developers
slug: Mozilla/Firefox/Releases/125
page-type: firefox-release-notes
---

{{FirefoxSidebar}}

This article provides information about the changes in Firefox 125 that affect developers. Firefox 125 is the current [Beta version of Firefox](https://www.mozilla.org/en-US/firefox/channel/desktop/#beta) and ships on [April 16, 2024](https://whattrainisitnow.com/release/?version=125).

## Changes for web developers

### Developer Tools

### HTML

#### Removals

### CSS

#### Removals

### JavaScript

- {{jsxref("Intl.Segmenter")}} is now supported, allowing developers to perform locale-sensitive text segmentation of a string.
  This enables, for example, splitting a string into words in languages that don't use spaces to separate them: `Intl.Segmenter("ja-JP", { granularity: "word" })`.
  You can also split strings into graphemes or sentences.
  ([Firefox bug 1423593](https://bugzil.la/1423593), [Firefox bug 1883914](https://bugzil.la/1883914).)

#### Removals

### SVG

#### Removals

### HTTP

#### Removals

### Security

#### Removals

### APIs

- The {{domxref("RTCIceTransport")}} properties {{domxref("RTCIceTransport/state","state")}} and {{domxref("RTCIceTransport/gatheringState","gatheringState")}}, and their associated events {{domxref("RTCIceTransport/statechange_event","statechange")}} and {{domxref("RTCIceTransport/gatheringstatechange_event","gatheringstatechange_event")}}, are now supported, along with the {{domxref("RTCDtlsTransport.iceTransport")}} property (which returns the underlying `RTCIceTransport` for a {{domxref("RTCDtlsTransport")}}).
  These allow much finer-grained monitoring than provided by the {{domxref("RTCPeerConnection")}} properties {{domxref("RTCPeerConnection.iceGatheringState","iceGatheringState")}} and {{domxref("RTCPeerConnection.connectionState","connectionState")}}.
  ([Firefox bug 1811912](https://bugzil.la/1811912))
- {{domxref("Element.ariaBrailleLabel")}} and {{domxref("Element.ariaBrailleRoleDescription")}} are now supported, respectively reflecting the global ARIA HTML attributes [`aria-braillelabel`](/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-braillelabel) and [`aria-brailleroledescription`](/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-brailleroledescription). ([Firefox bug 1861201](https://bugzil.la/1861201)).

#### DOM

#### Media, WebRTC, and Web Audio

#### Removals

- The [`SVGAElement.text`](/en-US/docs/Web/API/SVGAElement#svgaelement.text) property has been removed. The {{domxref("Node.textContent", "textContent")}} property (inherited from `Node`) is broadly supported and should be used instead. ([Firefox bug 1880689](https://bugzil.la/1880689)).

### WebAssembly

#### Removals

### WebDriver conformance (WebDriver BiDi, Marionette)

#### General

#### WebDriver BiDi

#### Marionette

## Changes for add-on developers

### Removals

### Other

## Experimental web features

These features are newly shipped in Firefox 125 but are disabled by default. To experiment with them, search for the appropriate preference on the `about:config` page and set it to `true`. You can find more such features on the [Experimental features](/en-US/docs/Mozilla/Firefox/Experimental_features) page.

## Older versions

{{Firefox_for_developers}}
