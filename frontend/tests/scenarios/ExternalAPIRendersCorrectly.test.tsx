import Home from "~/routes/home";
import { test, expect } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "tests/server";
import { render } from "@testing-library/react";
import { screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import userEvent from "@testing-library/user-event";

test("AI API is not available", async () => {
  render(
    <MemoryRouter>
      <Home />
    </MemoryRouter>,
  );

  const statusMessage = await screen.findByText(/нейросети/i);
});

test("AI Response is displayed as expected", async () => {
  const user = userEvent.setup();
  server.use(
    http.get("http://127.0.0.1:8000/v1/external/ai/health", () => {
      return new HttpResponse(null, { status: 200 });
    }),
  );

  render(
    <MemoryRouter>
      <Home />
    </MemoryRouter>,
  );

  const generateButton = screen.getByRole("button", {
    name: /generate ai answer/i,
  });

  await user.click(generateButton);
  const responseField = await screen.findByText(/ai response/i);
  expect(responseField).toBeInTheDocument();
});
