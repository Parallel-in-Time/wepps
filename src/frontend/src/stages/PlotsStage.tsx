import { useState, useMemo } from 'react';
import { PlotsStageProp } from './Interfaces';

import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

import Plot from 'react-plotly.js';

function PlotModal(props: {
  plot: PlotsStageProp;
  toggleVisibility: Function;
}) {
  const plot = () => {
    if (props.plot.plot != null) {
      const p = JSON.parse(props.plot.plot);
      return (
        <Plot
          data={p.data}
          layout={p.layout}
          style={{ width: '100%', minHeight: '58vh' }}
          config={{ responsive: true }}
        />
      );
    } else {
      return (
        <div>
          <div className='uk-section uk-section-muted uk-text-center uk-text-muted'>
            No plot computed
          </div>
        </div>
      );
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: '5%',
        left: '5%',
        right: '5%',
        bottom: '5%',
        zIndex: 10000,
        overflow: 'auto',
        boxShadow: '0 5px 15px rgba(0, 0, 0, 0.08)',
      }}
      className='uk-container uk-container-expand uk-background-default'
    >
      <div className='uk-padding-small'>
        <h2 className='uk-title uk-margin-left'>{props.plot.title}</h2>

        <div>{plot()}</div>
        <div className='uk-section uk-section-xsmall uk-text-center'>
          <ReactMarkdown
            children={props.plot.caption}
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
          />
        </div>
        <p className='uk-text-center'>
          <button
            className='uk-button uk-button-primary uk-modal-close uk-width-4-5'
            type='button'
            onClick={() => props.toggleVisibility()}
          >
            Close
          </button>
        </p>

        <div style={{ position: 'absolute', right: '5px', top: '5px' }}>
          <button
            className='uk-button uk-button-default uk-modal-close'
            type='button'
            onClick={() => props.toggleVisibility()}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function PlotsStage(props: PlotsStageProp) {
  const [visibleModal, setVisibleModal] = useState(false);

  function toggleVisibility() {
    setVisibleModal((m) => !m);
  }

  function makePlot() {
    if (props.plot != null) {
      const p = JSON.parse(props.plot);
      return (
        <>
          <Plot
            data={p.data}
            layout={p.layout}
            style={{ width: '100%', minHeight: '20vh' }}
            config={{ responsive: true }}
          />

          <div className='uk-section uk-section-xsmall uk-text-center'>
            <ReactMarkdown
              children={props.caption}
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            />
          </div>

          <button
            className='uk-button uk-button-default uk-width-1-1'
            type='button'
            onClick={() => {
              toggleVisibility();
            }}
          >
            Full screen
          </button>
        </>
      );
    } else if (props.caption) {
      return (
        <div>
          <ReactMarkdown
            children={props.caption}
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
          />
        </div>
      );
    } else {
      return (
        <div>
          <div className='uk-section uk-section-muted uk-text-center uk-text-muted'>
            No plot computed
          </div>
        </div>
      );
    }
  }
  const plot = useMemo(() => {
    return makePlot();
  }, [props.plot]);

  const modal = visibleModal ? (
    <PlotModal plot={props} toggleVisibility={toggleVisibility} />
  ) : (
    <></>
  );

  return (
    <>
      <div>{modal}</div>
      <div>
        <div className='uk-heading-bullet uk-margin-small-top uk-text-bolder'>
          {props.title}
        </div>
        {plot}
        <hr />
      </div>
    </>
  );
}

export default PlotsStage;
