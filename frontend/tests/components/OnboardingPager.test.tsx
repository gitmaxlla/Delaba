import { test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import OnboardingPager from "~/components/OnboardingPager";

test("OnboardingPager shows text", async () => {
  const user = userEvent.setup();
  render(<OnboardingPager />);
  expect(screen.getByText(/лаба/i)).toBeInTheDocument();

  const nextButton = screen.getByRole("generic", { name: /page 2/i });
  await user.click(nextButton);
  expect(screen.getByText(/задания/i)).toBeInTheDocument();
});
