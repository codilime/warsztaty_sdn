import {TranslationFunction} from 'i18next';
import {IObservableObject} from 'mobx';

export interface TDialogProps {
  data?: IObservableObject | object;
  schema?: IObservableObject;
  message?: IObservableObject;
  title?: string;
  errorMessage?: any;
  method?: string;
  t?: TranslationFunction;
  dialogId: string;
  isDialogOpen: boolean;
  isInProgress: boolean;
  save(id: string, data?: object): void;
  cancel(id: string): void;
}
