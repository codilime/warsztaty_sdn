export interface IConfig {
  authDomain: string;
  serverUrl: string;
  filteredRoles: string[];
}

export interface IConfigStore extends IConfig {
  isLoading: boolean;

  fetch(): Promise<any>;
}
