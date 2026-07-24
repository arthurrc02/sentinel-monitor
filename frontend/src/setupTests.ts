import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

import "@testing-library/jest-dom/vitest";

// Sem `test.globals: true` no vitest.config, o React Testing Library não detecta
// `afterEach` automaticamente — sem isso, componentes de um teste ficam montados
// no DOM quando o próximo teste roda.
afterEach(() => {
  cleanup();
});
