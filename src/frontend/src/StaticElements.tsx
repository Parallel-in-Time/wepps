import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

function HomeButton() {
  return (
    <div style={{ position: 'absolute', left: '5px', top: '5px' }}>
      <a href='/'>
        <span className='uk-margin-small-right' data-uk-icon='home'></span>
      </a>
    </div>
  );
}

function DocumentationButton(props: { toggleVisibility: Function }) {
  return (
    <div style={{ position: 'absolute', right: '5px', top: '5px' }}>
      <a
        onClick={() => {
          props.toggleVisibility();
        }}
      >
        <span className='uk-margin-small-right' data-uk-icon='info'></span>
      </a>
    </div>
  );
}

function DocumentationModal(props: {
  text: string;
  toggleVisibility: Function;
}) {
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
      className='uk-container uk-container-expand uk-background-default uk-padding-large'
    >
      <ReactMarkdown
        children={props.text}
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex]}
      />

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
  );
}

export { HomeButton, DocumentationButton, DocumentationModal };
