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
import { ReloadIcon } from "@radix-ui/react-icons";

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

  const [radiantHeroes, setRadiantHeroes] = useState<Hero[]>([]);
  const [direHeroes, setDireHeroes] = useState<Hero[]>([]);
  const [avgRankTier, setAvgRankTier] = useState<number>();

  const [predictedResult, setPredictedResult] = useState<string>("");

  const [isFetching, setIsFetching] = useState(false);

  const handleRadiantHeroUpdate = (hero: Hero | undefined, index: number) => {
    setRadiantHeroes((prev) => {
      if (hero === undefined) {
        return prev.filter((_, i) => i !== index);
      }

      prev[index] = hero;
      return prev;
    });
  };

  const handleDireHeroUpdate = (hero: Hero | undefined, index: number) => {
    setDireHeroes((prev) => {
      if (hero === undefined) {
        return prev.filter((_, i) => i !== index);
      }

      prev[index] = hero;
      return prev;
    });
  };

  const handleAvgRankTierUpdate = (tier: string) => {
    const parsedTier = parseInt(tier);

    if (isNaN(parsedTier)) {
      throw new Error("Invalid tier");
    }

    setAvgRankTier(parsedTier);
  };

  useEffect(() => {
    // Fetch heroes from API https://api.opendota.com/api/heroes

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
  }, []);

  const submitPredictHandler = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsFetching(true);
    // Merge the radiant and dire heroes into a single array of ids

    const ids = radiantHeroes.concat(direHeroes).map((hero) => hero.id);

    // Call the API to predict the match result
    let response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ids: ids,
        avg_rank_tier: avgRankTier,
      }),
    });

    let data = await response.json();
    setPredictedResult(data.radiant_win_prediction);
    setIsFetching(false);
  };

  const isFormValid = () => {
    if (radiantHeroes.length < 5) {
      return false;
    }

    if (direHeroes.length < 5) {
      return false;
    }

    if (!avgRankTier) {
      return false;
    }

    return true;
  };

  return (
    <form
      className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900"
      onSubmit={submitPredictHandler}
    >
      <h1 className="text-3xl font-bold">322 Bet</h1>
      <h2 className="text-2xl font-bold">Dota 2 Match Predictor</h2>
      <h3 className="text-sm font-light mb-10 text-gray-400">
        Current success rate: 58.86%
      </h3>
      <div className="grid grid-cols-2 gap-10 w-full max-w-3xl p-4 bg-white rounded-lg shadow-md dark:bg-gray-800">
        <div>
          <h2 className="text-xl font-semibold mb-4">Radiant</h2>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <HeroComboBox
                key={index}
                heroes={heroes}
                onUpdate={handleRadiantHeroUpdate}
                index={index}
              />
            ))}
          </div>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-4">Dire</h2>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <HeroComboBox
                key={index}
                heroes={heroes}
                onUpdate={handleDireHeroUpdate}
                index={index}
              />
            ))}
          </div>
        </div>
      </div>
      <div className="w-full max-w-3xl mt-10">
        <h2 className="text-xl font-semibold mb-4">Average Tier</h2>
        <Select onValueChange={handleAvgRankTierUpdate}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select average tier" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              {Object.entries(rankTiers).map(([key, value]) => {
                return Array.from({ length: value[1] - value[0] + 1 }).map(
                  (_, index) => (
                    <SelectItem
                      key={value[0] + index}
                      value={`${value[0] + index}`}
                    >
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
      {predictedResult && (
        <div className="w-full max-w-3xl mt-10  bg-white rounded-lg shadow-md dark:bg-gray-800 p-4">
          <h2 className="text-xl font-semibold mb-4">Prediction</h2>
          {parseFloat(predictedResult) > 0.5 ? (
            <span className="text-3xl font-semibold">
              Radiant wins with {(parseFloat(predictedResult) * 100).toFixed(2)}
              %
            </span>
          ) : (
            <span className="text-3xl font-semibold">
              Dire wins with{" "}
              {((1 - parseFloat(predictedResult)) * 100).toFixed(2)}%
            </span>
          )}
        </div>
      )}
      <PredictButton isFetching={isFetching} disabled={!isFormValid()} />
    </form>
  );
}

const PredictButton: React.FC<{
  isFetching: boolean;
  disabled: boolean;
}> = ({ isFetching, disabled }) => {
  if (isFetching) {
    return (
      <Button className="mt-10" disabled>
        <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />
        Please wait
      </Button>
    );
  }

  return (
    <Button className="mt-10" disabled={disabled}>
      Predict Match Result
    </Button>
  );
};

interface HeroComboBoxProps {
  heroes: Hero[];
  onUpdate: (value: Hero | undefined, index: number) => void;
  index: number;
}

const HeroComboBox: React.FC<HeroComboBoxProps> = ({
  heroes,
  onUpdate,
  index,
}) => {
  const [value, setValue] = useState<string>();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!heroes.length) {
      return;
    }

    const selectedHero = heroes.find((hero) => hero.name === value);

    onUpdate(selectedHero, index);
  }, [value]);

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
