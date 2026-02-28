import React from "react";
import { afterEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

vi.mock("@shoelace-style/shoelace/dist/react/icon/index.js", () => ({
  default: (props) =>
    React.createElement("span", { ...props, "data-testid": "sl-icon" }),
}));

vi.mock("@shoelace-style/shoelace/dist/react/menu/index.js", () => ({
  default: ({ children, ...props }) =>
    React.createElement("div", props, children),
}));

vi.mock("@shoelace-style/shoelace/dist/react/divider/index.js", () => ({
  default: (props) => React.createElement("hr", props),
}));

vi.mock("@shoelace-style/shoelace/dist/react/menu-item/index.js", () => ({
  default: ({ children, onClick, ...props }) =>
    React.createElement(
      "button",
      { type: "button", onClick, ...props },
      children,
    ),
}));

vi.mock("@shoelace-style/shoelace/dist/react/dropdown/index.js", () => ({
  default: ({
    children,
    onSlShow,
    onSlHide,
    onSlAfterHide,
    hoist: _hoist,
    ...props
  }) =>
    React.createElement(
      "div",
      {
        ...props,
        onMouseEnter: onSlShow,
        onMouseLeave: (event) => {
          onSlHide?.(event);
          onSlAfterHide?.(event);
        },
      },
      children,
    ),
}));

vi.mock("@shoelace-style/shoelace/dist/react/dialog/index.js", () => ({
  default: ({ children, open, label, onSlAfterHide, ...props }) =>
    open
      ? React.createElement(
          "div",
          {
            role: "dialog",
            "aria-label": label,
            onAnimationEnd: (event) => onSlAfterHide?.(event),
            ...props,
          },
          children,
        )
      : null,
}));

vi.mock("@shoelace-style/shoelace/dist/react/button/index.js", () => ({
  default: ({ children, pill: _pill, ...props }) =>
    React.createElement("button", { type: "button", ...props }, children),
}));

vi.mock("@shoelace-style/shoelace/dist/react/input/index.js", () => ({
  default: ({
    onSlInput,
    onChange,
    value,
    pill: _pill,
    autocomplete,
    autocorrect,
    autocapitalize,
    spellCheck,
    ...props
  }) =>
    React.createElement("input", {
      ...props,
      value: value ?? "",
      autoComplete: autocomplete,
      autoCorrect: autocorrect,
      autoCapitalize: autocapitalize,
      spellCheck,
      onChange: (event) => {
        onSlInput?.(event);
        onChange?.(event);
      },
    }),
}));
