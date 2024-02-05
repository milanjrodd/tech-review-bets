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
import { useState } from "react";

const HEROES_MOCK = [
  { name: "Abaddon", id: 1 },
  { name: "Alchemist", id: 2 },
  { name: "Ancient Apparition", id: 3 },
  { name: "Anti-Mage", id: 4 },
  { name: "Arc Warden", id: 5 },
  { name: "Axe", id: 6 },
  { name: "Bane", id: 7 },
  { name: "Batrider", id: 8 },
  { name: "Beastmaster", id: 9 },
  { name: "Bloodseeker", id: 10 },
  { name: "Bounty Hunter", id: 11 },
  { name: "Brewmaster", id: 12 },
  { name: "Bristleback", id: 13 },
  { name: "Broodmother", id: 14 },
  { name: "Centaur Warrunner", id: 15 },
  { name: "Chaos Knight", id: 16 },
  { name: "Chen", id: 17 },
  { name: "Clinkz", id: 18 },
  { name: "Clockwerk", id: 19 },
  { name: "Crystal Maiden", id: 20 },
  { name: "Dark Seer", id: 21 },
  { name: "Dark Willow", id: 22 },
  { name: "Dazzle", id: 23 },
  { name: "Death Prophet", id: 24 },
  { name: "Disruptor", id: 25 },
  { name: "Doom", id: 26 },
  { name: "Dragon Knight", id: 27 },
  { name: "Drow Ranger", id: 28 },
  { name: "Earth Spirit", id: 29 },
  { name: "Earthshaker", id: 30 },
  { name: "Elder Titan", id: 31 },
  { name: "Ember Spirit", id: 32 },
  { name: "Enchantress", id: 33 },
  { name: "Enigma", id: 34 },
  { name: "Faceless Void", id: 35 },
  { name: "Grimstroke", id: 36 },
  { name: "Gyrocopter", id: 37 },
  { name: "Hoodwink", id: 38 },
  { name: "Huskar", id: 39 },
  { name: "Invoker", id: 40 },
  { name: "Io", id: 41 },
  { name: "Jakiro", id: 42 },
  { name: "Juggernaut", id: 43 },
  { name: "Keeper of the Light", id: 44 },
  { name: "Kunkka", id: 45 },
  { name: "Legion Commander", id: 46 },
  { name: "Leshrac", id: 47 },
  { name: "Lich", id: 48 },
  { name: "Lifestealer", id: 49 },
  { name: "Lina", id: 50 },
  { name: "Lion", id: 51 },
  { name: "Lone Druid", id: 52 },
  { name: "Luna", id: 53 },
  { name: "Lycan", id: 54 },
  { name: "Magnus", id: 55 },
  { name: "Mars", id: 56 },
  { name: "Medusa", id: 57 },
  { name: "Meepo", id: 58 },
  { name: "Mirana", id: 59 },
  { name: "Monkey King", id: 60 },
  { name: "Morphling", id: 61 },
  { name: "Naga Siren", id: 62 },
  { name: "Nature's Prophet", id: 63 },
  { name: "Necrophos", id: 64 },
  { name: "Night Stalker", id: 65 },
  { name: "Nyx Assassin", id: 66 },
  { name: "Ogre Magi", id: 67 },
  { name: "Omniknight", id: 68 },
  { name: "Oracle", id: 69 },
  { name: "Outworld Destroyer", id: 70 },
  { name: "Pangolier", id: 71 },
  { name: "Phantom Assassin", id: 72 },
  { name: "Phantom Lancer", id: 73 },
  { name: "Phoenix", id: 74 },
  { name: "Puck", id: 75 },
  { name: "Pudge", id: 76 },
  { name: "Pugna", id: 77 },
  { name: "Queen of Pain", id: 78 },
  { name: "Razor", id: 79 },
  { name: "Riki", id: 80 },
  { name: "Rubick", id: 81 },
  { name: "Sand King", id: 82 },
  { name: "Shadow Demon", id: 83 },
  { name: "Shadow Fiend", id: 84 },
  { name: "Shadow Shaman", id: 85 },
  { name: "Silencer", id: 86 },
  { name: "Skywrath Mage", id: 87 },
  { name: "Slardar", id: 88 },
  { name: "Slark", id: 89 },
  { name: "Snapfire", id: 90 },
  { name: "Sniper", id: 91 },
  { name: "Spectre", id: 92 },
  { name: "Spirit Breaker", id: 93 },
  { name: "Storm Spirit", id: 94 },
  { name: "Sven", id: 95 },
  { name: "Techies", id: 96 },
  { name: "Templar Assassin", id: 97 },
  { name: "Terrorblade", id: 98 },
  { name: "Tidehunter", id: 99 },
  { name: "Timbersaw", id: 100 },
  { name: "Tinker", id: 101 },
  { name: "Tiny", id: 102 },
  { name: "Treant Protector", id: 103 },
  { name: "Troll Warlord", id: 104 },
  { name: "Tusk", id: 105 },
  { name: "Underlord", id: 106 },
  { name: "Undying", id: 107 },
  { name: "Ursa", id: 108 },
  { name: "Vengeful Spirit", id: 109 },
  { name: "Venomancer", id: 110 },
  { name: "Viper", id: 111 },
  { name: "Visage", id: 112 },
  { name: "Void Spirit", id: 113 },
  { name: "Warlock", id: 114 },
  { name: "Weaver", id: 115 },
  { name: "Windranger", id: 116 },
  { name: "Winter Wyvern", id: 117 },
  { name: "Witch Doctor", id: 118 },
  { name: "Wraith King", id: 119 },
  { name: "Zeus", id: 120 },
];

export default function PredictComponent() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <h1 className="text-3xl font-bold">322 Bet</h1>
      <h1 className="text-2xl font-bold mb-10">Dota 2 Match Predictor</h1>
      <div className="grid grid-cols-2 gap-10 w-full max-w-3xl p-4 bg-white rounded-lg shadow-md dark:bg-gray-800">
        <div>
          <h2 className="text-xl font-semibold mb-4">Radiant</h2>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <HeroComboBox key={index} heroes={HEROES_MOCK} />
            ))}
          </div>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-4">Dire</h2>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <HeroComboBox key={index} heroes={HEROES_MOCK} />
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
              <SelectItem value="1">Tier 1</SelectItem>
              <SelectItem value="2">Tier 2</SelectItem>
              <SelectItem value="3">Tier 3</SelectItem>
              <SelectItem value="4">Tier 4</SelectItem>
              <SelectItem value="5">Tier 5</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
      <Button className="mt-10">Predict Match Result</Button>
    </div>
  );
}

interface HeroComboBoxProps {
  heroes: { name: string; id: number }[];
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
            ? HEROES_MOCK.find(
                (hero) => hero.name.toLocaleLowerCase() === value
              )?.name
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
                {hero.name}
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
