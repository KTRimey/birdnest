import React from "react";
import { screen } from "@testing-library/react";
import { render } from "./test-utils";
import { App } from "./App";

test("renders page", () => {
  render(<App />);
  const helloWorld = screen.getByText(/Hello, World!/i);
  expect(helloWorld).toBeInTheDocument();
});
