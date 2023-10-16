import { DocsComponentsProps } from './Interfaces';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

function DocsComponent(props: DocsComponentsProps) {
  return (
    <>
      <div className='uk-grid-small uk-child-width-1-1' data-uk-grid>
        <div className='uk-heading-bullet uk-margin-small-top uk-text-bolder uk-first-column'>
          {props.title}
        </div>
        <div>
          <ReactMarkdown
            children={props.text}
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
          />
        </div>
      </div>
    </>
  );
}
export default DocsComponent;
