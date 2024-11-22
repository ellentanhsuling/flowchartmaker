import streamlit as st
import graphviz
import json

# [Previous functions remain unchanged]

def main():
    st.title('Editable Violent Incident Management Protocol')
    
    # Add main instructions
    st.markdown("""
    ### How to Use This App
    This flowchart editor allows you to customize the Violent Incident Management Protocol.
    
    **Main Features:**
    - View the flowchart in the main area
    - Edit nodes and connections in the sidebar
    - Export/Import your customized flowchart
    """)
    
    # Initialize session state for nodes and edges
    if 'nodes' not in st.session_state:
        st.session_state.nodes = load_default_nodes()
    if 'edges' not in st.session_state:
        st.session_state.edges = load_default_edges()
    
    # Sidebar for editing
    with st.sidebar:
        st.header('Edit Flowchart')
        
        # Add sidebar instructions
        st.markdown("""
        #### Instructions:
        1. **Edit Nodes**: Modify existing node text
        2. **Edit Edges**: Change connections between nodes
        3. **Add New Node**: 
           - Enter a unique ID (e.g., 'R', 'S')
           - Add node description
           - Click 'Add Node'
        4. **Add New Edge**:
           - Enter source node ID
           - Enter target node ID
           - Add optional label
           - Click 'Add Edge'
        """)
        
        # Edit nodes
        st.subheader('Edit Nodes')
        st.info('Edit the text for each node below:')
        for node_id in st.session_state.nodes:
            st.session_state.nodes[node_id] = st.text_area(
                f'Node {node_id}',
                st.session_state.nodes[node_id],
                key=f'node_{node_id}'
            )
        
        # Edit edges
        st.subheader('Edit Edges')
        st.info('Modify connections between nodes:')
        for idx, (source, target, label) in enumerate(st.session_state.edges):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_source = st.text_input(f'Source {idx}', source, key=f'source_{idx}')
            with col2:
                new_target = st.text_input(f'Target {idx}', target, key=f'target_{idx}')
            with col3:
                new_label = st.text_input(f'Label {idx}', label, key=f'label_{idx}')
            st.session_state.edges[idx] = (new_source, new_target, new_label)
        
        # Add new node
        st.subheader('Add New Node')
        st.info('Create a new step in the protocol:')
        new_node_id = st.text_input('New Node ID')
        new_node_label = st.text_area('New Node Label')
        if st.button('Add Node') and new_node_id and new_node_label:
            st.session_state.nodes[new_node_id] = new_node_label
        
        # Add new edge
        st.subheader('Add New Edge')
        st.info('Connect nodes with a new line:')
        new_edge_source = st.text_input('New Edge Source')
        new_edge_target = st.text_input('New Edge Target')
        new_edge_label = st.text_input('New Edge Label')
        if st.button('Add Edge') and new_edge_source and new_edge_target:
            st.session_state.edges.append((new_edge_source, new_edge_target, new_edge_label))
        
        # Export/Import functionality
        st.subheader('Export/Import')
        st.info('Save or load your customized flowchart:')
        if st.button('Export Configuration'):
            config = {
                'nodes': st.session_state.nodes,
                'edges': st.session_state.edges
            }
            st.download_button(
                'Download Configuration',
                json.dumps(config),
                'flowchart_config.json'
            )
        
        uploaded_file = st.file_uploader('Import Configuration')
        if uploaded_file is not None:
            config = json.loads(uploaded_file.getvalue())
            st.session_state.nodes = config['nodes']
            st.session_state.edges = config['edges']
            st.success('Configuration imported successfully!')
    
    # Display the flowchart
    st.subheader('Current Flowchart')
    st.info('The flowchart updates automatically as you make changes in the sidebar.')
    flowchart = create_flowchart(st.session_state.nodes, st.session_state.edges)
    st.graphviz_chart(flowchart)

if __name__ == '__main__':
    main()
