import streamlit as st
import streamlit.components.v1 as components
from allennlp.predictors.predictor import Predictor
import allennlp_models.rc

st.markdown('# MIT Policy Pal')
st.markdown('#### Made with :heart: by Jake, Jenny, and Raunak!')
st.markdown('')

mode = st.sidebar.selectbox(
    "Operation Mode",
    ("Learn", "Play")
)


if mode == 'Learn':
    @st.cache(allow_output_mutation=True)
    def get_predictor():
        with st.spinner('Loading a large model to memory (might take a bit)...'):
            return Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2020.03.19.tar.gz")

    predictor = get_predictor()

    with open('policy.txt', 'r') as f:
        context = f.read()

    headers = []
    line_nums = []

    skip = {'A', 'MIT', '*NOTE:', 'PLEASE NOTE:'}

    context_lines = context.split('\n')
    for line_num, line in enumerate(context_lines):
        try:
            if line.split()[0].isupper():

                title = []
                for word in line.split():
                    if not word.isupper():
                        break
                    title.append(word)

                if ' '.join(title) in skip:
                    continue

                headers.append(' '.join(title))
                line_nums.append(line_num)
        except:
            pass




    sections = {}
    for header, line_start, line_end in zip(headers, line_nums, line_nums[1:]):
        sections[header.title()] = ' '.join(context_lines[line_start+1:line_end])

    header_section = st.selectbox('Select which policy section you have a question about',tuple(sections.keys()))  # user will select which section
    context = sections[header_section]
    question = st.text_input('Enter your question here:')
    if st.button('Press Here to Ask!'):
        out = predictor.predict(
            passage=context,
            question=question
        )

        sentences = context.replace(out['best_span_str'], 'BDE MFs').split('.')
        sentence_num = -1
        for i, sent in enumerate(sentences):
            if 'BDE MFs' in sent:
                sentence_num = i
                break

        ret = '.'.join(sentences[max(0,sentence_num-1):sentence_num+2]).replace('BDE MFs', '**' + out['best_span_str'] + '**')
        st.success(ret)

        st.info("If our bot couldn't answer your question properly, please email [the UA COVID-19 Team](mailto:ua-covid19@mit.edu) with any additional questions you might have.")

    st.markdown('## Reporting')
    with st.beta_expander('MIT Student Reporting Hotline'):
        st.markdown('If students are concerned about the behaviors of other students relative to COVID-19 and health risks, they can report this information through this COVID-19 Public Health Concern Report Form.')
        components.iframe('https://cm.maxient.com/reportingform.php?MassInstofTech&layout_id=12', height=1000, scrolling=True)
    with st.beta_expander('MIT Non-Student Reporting Hotline'):
        st.markdown('Concerns about the behaviors of non-student members relative to COVID-19 and health risks may be reported to this MIT Hotline.')
        col1, col2 = st.beta_columns(2)
        with col1:
            image = 'data:image/png;base64,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'
            link = f'[![this is an image link]({image})](https://secure.ethicspoint.com/domain/media/en/gui/28258/index.html)'
            st.markdown(link, unsafe_allow_html=True)
        with col2:
            st.error('**This is not an emergency line.**  If you have an emergency, please dial 617-253-1212 or 100 from a campus phone.  If you are off campus, please dial 911.')
        st.markdown("""
    MIT has established an anonymous reporting hotline for whistleblower or other complaints about wrongdoing and violations of Institute policy. The reporting system is hosted and maintained by a third-party vendor called Ethicspoint. 

    There are many other ways to report issues around the Institute. In many cases, MIT is better able to respond to complaints that are not anonymous.

    Anyone may use the hotline to report a concern about suspected wrongdoing in the MIT community. The most common categories for hotline reports are the following:
    - COVID-19
    - Conflicts of Interest
    - Environmental Health & Safety
    - Financial
    - Human Resources (including discrimination and harassment)
    - Information Technology
    - Research
    - Risk and Safety
    - Violations of Law, Contract, or MIT Policy""")
        st.markdown(' ')

    with st.beta_expander('Provide Anonymous Policy Feedback'):
        'The administration understands that our policies may not perfectly addressed the needs of all students, and is open to receiving feedback, suggestions, and even complaints related to its policies. Fill out this form to log your feedback, and it will be anonymously processed through MIT UA and shared with administrators.'
        st.text_input('Optional: Email for Response')
        st.text_area(label='Feedback')
        if st.button('Send Anonymous Report'):
            st.success('Your report has been sent. Thank you for helping making MIT safer!')

    st.markdown(' ')
    st.markdown(' ')
    '## Reference Policies'

    for header_section, content in sections.items():
        with st.beta_expander(header_section):
            st.markdown(content)
else:
    'We encourage students to design custom Kahoot and skribbl.io games based on the MIT COVID policies. We might hold competitions with prizes for those who created the games and those who won the competition! You can enter the codes for some of these games below to play them right in our web app."
    with st.beta_expander('Kahoot Quiz', expanded=True):
        components.iframe('https://kahoot.it/', height=500)
    with st.beta_expander('Skribbl.io Game', expanded=True):
        components.iframe('https://skribbl.io/', height=1000)    
