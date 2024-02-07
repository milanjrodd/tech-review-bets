/**
 * v0 by Vercel.
 * @see https://v0.dev/t/lQWW4eZIfqc
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { Button } from "@/components/ui/button";
import {
  PopoverTrigger,
  PopoverContent,
  Popover,
} from "@/components/ui/popover";
import {
  CommandInput,
  CommandEmpty,
  CommandItem,
  CommandGroup,
  Command,
} from "@/components/ui/command";
import {
  SelectValue,
  SelectTrigger,
  SelectItem,
  SelectGroup,
  SelectContent,
  Select,
} from "@/components/ui/select";
import { useEffect, useState } from "react";
import type { Hero } from "@/types/heroes";

const rankTiers = {
  herald: [10, 15],
  guardian: [20, 25],
  crusader: [30, 35],
  archon: [40, 45],
  legend: [50, 55],
  ancient: [60, 65],
  divine: [70, 75],
  immortal: [80, 85],
};

export default function PredictComponent() {
  const [heroes, setHeroes] = useState<Hero[]>([]);
  useEffect(() => {
    (async () => {
      let headersList = {
        Accept: "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
      };

      let response = await fetch("https://api.opendota.com/api/heroes", {
        method: "GET",
        headers: headersList,
      });

      let data: Hero[] = await response.json();

      setHeroes(data);
    })();
    // Fetch heroes from API https://api.opendota.com/api/heroes
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <h1 className="text-3xl font-bold">322 Bet</h1>
      <h1 className="text-2xl font-bold mb-10">Dota 2 Match Predictor</h1>
      <div className="grid grid-cols-2 gap-10 w-full max-w-3xl p-4 bg-white rounded-lg shadow-md dark:bg-gray-800">
        <div>
          <h2 className="text-xl font-semibold mb-4">Radiant</h2>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <HeroComboBox key={index} heroes={heroes} />
            ))}
          </div>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-4">Dire</h2>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <HeroComboBox key={index} heroes={heroes} />
            ))}
          </div>
        </div>
      </div>
      <div className="w-full max-w-3xl mt-10">
        <h2 className="text-xl font-semibold mb-4">Average Tier</h2>
        <Select>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select average tier" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              {Object.entries(rankTiers).map(([key, value]) => {
                return Array.from({ length: value[1] - value[0] + 1 }).map(
                  (_, index) => (
                    <SelectItem key={index} value={`${key}_${index}`}>
                      {key.charAt(0).toUpperCase() + key.slice(1)} (
                      {value[0] + index})
                    </SelectItem>
                  )
                );
              })}
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
      <Button className="mt-10">Predict Match Result</Button>
    </div>
  );
}

interface HeroComboBoxProps {
  heroes: Hero[];
}

const HeroComboBox: React.FC<HeroComboBoxProps> = ({ heroes }) => {
  const [value, setValue] = useState<string>();
  const [open, setOpen] = useState(false);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          className="w-full justify-between"
          role="combobox"
          variant="outline"
        >
          {value
            ? heroes.find((hero) => hero.name === value)?.localized_name
            : "Select Hero..."}

          <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full h-72 p-0">
        <Command>
          <CommandInput className="h-9" placeholder="Search hero..." />
          <CommandEmpty>No hero found.</CommandEmpty>
          <CommandGroup>
            {heroes.map((hero, id) => (
              <CommandItem
                key={hero.id}
                value={hero.name}
                onSelect={(currentValue) => {
                  setValue(currentValue === value ? "" : currentValue);
                  setOpen(false);
                }}
              >
                {hero.localized_name}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
};

function ChevronsUpDownIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m7 15 5 5 5-5" />
      <path d="m7 9 5-5 5 5" />
    </svg>
  );
}
