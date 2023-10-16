import Parameter from './Parameter';

import { ParameterProp } from '../Interfaces';
import { useMemo } from 'react';

function ParameterList(props: {
  parameters: Array<ParameterProp>;
  updateParameter: Function;
}) {
  const parameters = useMemo(
    () =>
      props.parameters.map((parameter, i) => (
        <Parameter
          id={parameter.id}
          name={parameter.name}
          placeholder={parameter.placeholder}
          doc={parameter.doc}
          type={parameter.type}
          choices={parameter.choices}
          value={parameter.value}
          updateParameter={props.updateParameter}
          key={i}
        />
      )),
    [props.parameters]
  );

  return <>{parameters}</>;
}

export default ParameterList;
