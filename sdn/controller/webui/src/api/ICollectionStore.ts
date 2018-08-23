import {IBaseStore} from './';

export interface ICollectionStore extends IBaseStore {
  data: object[];
  totalCount: number;
  query: object;

  fetch(query?: object, headers?: object): void;
}
