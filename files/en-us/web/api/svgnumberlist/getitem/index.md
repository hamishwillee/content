---
title: "SVGNumberList: getItem() method"
short-title: getItem()
slug: Web/API/SVGNumberList/getItem
page-type: web-api-instance-method
browser-compat: api.SVGNumberList.getItem
---

{{APIRef("SVG")}}

The **`getItem()`** method of the {{domxref("SVGNumberList")}} interface returns the specified item from the list. The returned item is the item itself and not a copy. Any changes made to the item are immediately reflected in the list. The first item is indexed 0.

## Syntax

```js-nolint
getItem(index)
```

### Parameters

- `index`
  - : A non-negative integer that specifies the index of the item to retrieve.

### Return value

The {{domxref("SVGNumber")}} at the specified index in the list.

### Exceptions

- {{domxref("DOMException")}} `IndexSizeError`
  - : Thrown when the index is out of bounds for the list.

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}
