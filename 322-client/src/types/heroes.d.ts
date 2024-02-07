export interface Hero {
  id: number;
  name: string;
  localized_name: string;
  primary_attr: PrimaryAttr;
  attack_type: AttackType;
  roles: Role[];
  legs: number | null;
}

export enum AttackType {
  Melee = "Melee",
  Ranged = "Ranged",
}

export enum PrimaryAttr {
  Agi = "agi",
  All = "all",
  Int = "int",
  Str = "str",
}

export enum Role {
  Carry = "Carry",
  Disabler = "Disabler",
  Durable = "Durable",
  Escape = "Escape",
  Initiator = "Initiator",
  Nuker = "Nuker",
  Pusher = "Pusher",
  Support = "Support",
}
