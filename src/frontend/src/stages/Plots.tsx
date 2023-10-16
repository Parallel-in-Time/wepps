import PlotsStage from './PlotsStage';

import { PlotsProp } from './Interfaces';

import { useMemo } from 'react';

function Plots(props: PlotsProp) {
  const plots = useMemo(
    () =>
      props.plots.map((element, i) => (
        <PlotsStage
          title={element.title}
          caption={element.caption}
          plot={element.plot}
          key={i}
        />
      )),
    [props.plots]
  );

  return (
    <div>
      <div className='uk-card uk-card-body uk-card-default uk-card-hover'>
        <div className='uk-child uk-child-width-1-1' data-uk-grid>
          <div className='uk-grid-collapse uk-child-width-1-1' data-uk-grid>
            {plots}
          </div>
        </div>
      </div>
    </div>
  );
}
export default Plots;
