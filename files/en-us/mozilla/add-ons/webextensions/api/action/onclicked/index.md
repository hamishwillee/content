---
title: action.onClicked
slug: Mozilla/Add-ons/WebExtensions/API/action/onClicked
page-type: webextension-api-event
browser-compat: webextensions.api.action.onClicked
sidebar: addonsidebar
---

Fired when a browser action icon is clicked. This event will not fire if the browser action has a popup.

> [!NOTE]
> This API is available in Manifest V3 or higher.

To define a right-click action, use the [`contextMenus`](/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus) API with the "browser_action" [context type](/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus/ContextType).

## Syntax

```js-nolint
browser.action.onClicked.addListener(listener)
browser.action.onClicked.removeListener(listener)
browser.action.onClicked.hasListener(listener)
```

Events have three functions:

- `addListener(listener)`
  - : Adds a listener to this event.
- `removeListener(listener)`
  - : Stop listening to this event. The `listener` argument is the listener to remove.
- `hasListener(listener)`
  - : Check whether `listener` is registered for this event. Returns `true` if it is listening, `false` otherwise.

## addListener syntax

### Parameters

- `listener`
  - : The function called when this event occurs. The function is passed these arguments:
    - `tab`
      - : {{WebExtAPIRef('tabs.Tab')}}. The tab that was active when the icon was clicked.
    - `OnClickData`
      - : An object containing information about the click.
        - `modifiers`
          - : An `array`. The keyboard modifiers active at the time of the click, being one or more of `Shift`, `Alt`, `Command`, `Ctrl`, or `MacCtrl`.
        - `button`
          - : An `integer`. Indicates the button used to click the page action icon: `0` for a left-click or a click not associated with a mouse, such as one from the keyboard and `1` for a middle button or wheel click. Note that the right-click is not supported because Firefox consumes that click to display the context menu before this event is triggered.

## Examples

When the user clicks the icon, disable it for the active tab, and log the tab's URL:

```js
browser.action.onClicked.addListener((tab) => {
  // disable the active tab
  browser.action.disable(tab.id);
  // requires the "tabs" or "activeTab" permission, or host permissions for the URL
  console.log(tab.url);
});
```

{{WebExtExamples}}

## Browser compatibility

{{Compat}}

> [!NOTE]
> This API is based on Chromium's [`chrome.action`](https://developer.chrome.com/docs/extensions/reference/api/action#event-onClicked) API. This documentation is derived from [`browser_action.json`](https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/api/browser_action.json) in the Chromium code.

<!--
// Copyright 2015 The Chromium Authors. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//    * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//    * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//    * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-->
