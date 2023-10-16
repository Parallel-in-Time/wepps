export interface DocsComponentsProps {
  title: string;
  id: string;
  text: string;
  activated: boolean;
  dependency: string;
}

export interface DocsProp {
  docs: Array<DocsComponentsProps>;
}

export interface SettingsStageProp {
  title: string;
  id: string;
  folded: boolean;
  parameters: Array<ParameterProp>;
  updateParameter: Function;
}

export interface SettingsProp {
  settings: Array<SettingsStageProp>;
  updateParameter: Function;
}

export interface PlotsStageProp {
  title: string;
  caption: string;
  plot: string;
}

export interface PlotsProp {
  plots: Array<PlotsStageProp>;
}

export interface ParameterProp {
  id: string;
  name: string;
  placeholder: string;
  doc: string;
  type: ParameterType;
  choices: Array<string>;
  value: string;
  updateParameter: Function;
}

export interface ParameterValue {
  id: string;
  name: string;
  value: string;
  isValid: boolean;
}

export enum ParameterType {
  Integer = 'Integer',
  PositiveInteger = 'PositiveInteger',
  StrictlyPositiveInteger = 'StrictlyPositiveInteger',
  PositiveFloat = 'PositiveFloat',
  Float = 'Float',
  Enumeration = 'Enumeration',
  FloatList = 'FloatList',
  Boolean = 'Boolean',
}
