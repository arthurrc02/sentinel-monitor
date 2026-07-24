import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ComputerStatusBadge } from "./ComputerStatusBadge";

describe("ComputerStatusBadge", () => {
  it("mostra 'Online' quando isOnline é true", () => {
    render(<ComputerStatusBadge isOnline={true} />);

    expect(screen.getByText("Online")).toBeInTheDocument();
  });

  it("mostra 'Offline' quando isOnline é false", () => {
    render(<ComputerStatusBadge isOnline={false} />);

    expect(screen.getByText("Offline")).toBeInTheDocument();
  });
});
