export interface IGlobalMessageStore {
  messages: TGlobalMessage[];

  push(message: string, type: string): void;
  remove(id: number): void;
}

export interface TGlobalMessage {
  id: number;
  message: boolean;
  type: string;
  show: boolean;
}
