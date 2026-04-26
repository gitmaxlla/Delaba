import { test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import OnboardingPager from "~/components/OnboardingPager";

test("OnboardingPager shows text", () => {
  render(<OnboardingPager />);
  expect(screen.getByText(/лаба/i)).toBeInTheDocument();
});
