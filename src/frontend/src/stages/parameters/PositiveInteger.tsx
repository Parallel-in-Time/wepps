import NumberField from './NumberField';

function checkValidity(v: string) {
  // @ts-expect-error
  return v !== '' && !isNaN(+v) && parseInt(v) == v && +v >= 0;
}

function PositiveInteger(props: {
  id: string;
  name: string;
  value: string;
  placeholder: string;
  doc: string;
  updateParameter: Function;
}) {
  return (
    <NumberField
      id={props.id}
      name={props.name}
      defaultValue={props.value}
      placeholder={props.placeholder}
      doc={props.doc}
      scalar={true}
      updateParameter={props.updateParameter}
      checkValidity={checkValidity}
    />
  );
}

export default PositiveInteger;
