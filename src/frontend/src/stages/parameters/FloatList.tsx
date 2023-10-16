import NumberField from './NumberField';

function checkValidity(vl: string) {
  const validity = vl
    .split(',')
    .map((v) => v.replace(/\s/g, '') !== '' && !isNaN(+v));
  return validity.every((v) => v === true);
}

function FloatList(props: {
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
      defaultValue={
        Array.isArray(props.value) ? String(props.value) : props.value
      }
      placeholder={props.placeholder}
      doc={props.doc}
      updateParameter={props.updateParameter}
      scalar={false}
      checkValidity={checkValidity}
    />
  );
}

export default FloatList;
