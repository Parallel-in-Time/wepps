import DocsComponent from './DocsComponent';
import { DocsProp } from './Interfaces';

import { useMemo } from 'react';

function Docs(props: DocsProp) {
  const components = useMemo(
    () =>
      props.docs.map((element, i) => (
        <DocsComponent
          title={element.title}
          id={element.id}
          text={element.text}
          activated={element.activated}
          dependency={element.dependency}
          key={i}
        />
      )),
    [props.docs]
  );

  return (
    <div className='uk-card uk-card-body uk-card-default uk-card-hover'>
      <div
        style={{
          overflow: 'auto',
        }}
      >
        <div className='uk-child uk-child-width-1-1' data-uk-grid>
          {components}
        </div>
      </div>
    </div>
  );
}
export default Docs;
