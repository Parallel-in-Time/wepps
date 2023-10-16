import { useContext, useEffect, useState } from 'react';
import { StageContext } from '../StageContext';

function Boolean(props: {
  id: string;
  name: string;
  value: boolean;
  placeholder: string;
  doc: string;
  updateParameter: Function;
}) {
  const initialValue = props.value != null ? props.value : false;
  const [value, setValue] = useState(initialValue);

  const stage = useContext(StageContext);

  const onChangeCallback = (v: boolean) => {
    setValue(v);
    props.updateParameter(stage, {
      id: props.id,
      name: props.name,
      value: v,
      isValid: true,
    });
  };

  // Set the default value if it changed in the props
  useEffect(() => {
    if (props.value !== value) {
      onChangeCallback(props.value);
    }
  }, [props.value]);

  useEffect(() => onChangeCallback(initialValue), []);

  return (
    <input
      uk-tooltip={`title: ${props.doc}`}
      className={`uk-checkbox uk-align-right`}
      defaultChecked={value}
      onChange={(e) => onChangeCallback(e.target.checked)}
      placeholder={props.placeholder}
      type='checkbox'
    />
  );
}

export default Boolean;
