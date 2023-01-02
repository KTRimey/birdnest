import { screen } from "@testing-library/react";
import { render } from "./test-utils";
import { App } from "./App";

test("renders page", () => {
  render(<App />);
  const title = screen.getByText(
    /Pilots who have recently violated the NDZ perimeter/i
  );
  expect(title).toBeInTheDocument();
});
