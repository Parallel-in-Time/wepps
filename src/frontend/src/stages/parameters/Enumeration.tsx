import { useContext, useEffect, useState } from 'react';
import { StageContext } from '../StageContext';

function Enumeration(props: {
  id: string;
  name: string;
  value: string;
  placeholder: string;
  choices: Array<string>;
  doc: string;
  updateParameter: Function;
}) {
  const initialValue = props.value == null ? props.choices[0] : props.value;
  const [value, setValue] = useState(initialValue);

  const stage = useContext(StageContext);

  const onChangeCallback = (v: string) => {
    setValue(v);
    props.updateParameter(stage, {
      id: props.id,
      name: props.name,
      value: v,
      isValid: true,
    });
  };

  useEffect(() => onChangeCallback(initialValue), []);

  const options = props.choices.map((choice, i) => {
    return (
      <option value={choice} key={i}>
        {choice}
      </option>
    );
  });

  return (
    <select
      id={`select-${props.id}`}
      className='uk-select'
      onChange={(e) => onChangeCallback(e.target.value)}
      data-uk-tooltip={`title: ${props.doc}`}
      value={value}
    >
      {options}
    </select>
  );
}

export default Enumeration;
