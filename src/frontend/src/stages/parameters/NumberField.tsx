import { useContext, useEffect, useState } from 'react';
import { StageContext } from '../StageContext';

function NumberField(props: {
  id: string;
  name: string;
  defaultValue: string;
  placeholder: string;
  doc: string;
  scalar: boolean;
  updateParameter: Function;
  checkValidity: Function;
}) {
  const initialValue = props.defaultValue != null ? props.defaultValue : '';
  const [value, setValue] = useState(initialValue);
  const [valid, setValid] = useState(props.checkValidity(initialValue));

  const stage = useContext(StageContext);

  const onChangeCallback = (v: string) => {
    setValue(v);
    // Valid if not empty, a number
    const isValid = props.checkValidity(v);
    setValid(isValid);
    props.updateParameter(stage, {
      id: props.id,
      name: props.name,
      value: isValid ? v : '',
      isValid: isValid,
    });
  };

  // Set the default value if it changed in the props
  useEffect(() => {
    if (props.defaultValue !== value) {
      const v = props.defaultValue != null ? props.defaultValue : '';
      onChangeCallback(v);
    }
  }, [props.defaultValue]);

  useEffect(() => onChangeCallback(initialValue), []);

  return (
    <input
      uk-tooltip={`title: ${props.doc}`}
      className={`uk-input uk-align-right ${valid ? '' : 'uk-form-danger'}`}
      type={props.scalar ? 'number' : ''}
      value={value}
      onChange={(e) => onChangeCallback(e.target.value)}
      placeholder={props.placeholder}
    />
  );
}

export default NumberField;
