import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { PollingIntervalSelect } from "./PollingIntervalSelect";

describe("PollingIntervalSelect", () => {
  it("mostra o valor selecionado atual", () => {
    render(<PollingIntervalSelect value={10_000} onChange={vi.fn()} />);

    const select = screen.getByLabelText("Atualizar a cada");
    expect(select).toHaveValue("10000");
  });

  it("chama onChange com o valor numérico ao escolher outra opção", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();
    render(<PollingIntervalSelect value={10_000} onChange={onChange} />);

    await user.selectOptions(screen.getByLabelText("Atualizar a cada"), "30000");

    expect(onChange).toHaveBeenCalledWith(30_000);
  });
});
