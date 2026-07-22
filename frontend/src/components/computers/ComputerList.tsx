import type { Computer } from "../../api/types";
import { ComputerCard } from "./ComputerCard";

interface ComputerListProps {
  computers: Computer[];
}

export function ComputerList({ computers }: ComputerListProps) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {computers.map((computer) => (
        <ComputerCard key={computer.id} computer={computer} />
      ))}
    </div>
  );
}
