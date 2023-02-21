# taken from https://gist.github.com/benlansdell/44000c264d1b373c77497c0ea73f0ef2
# slightly modified
"""FilePicker for streamlit. 

Still doesn't seem to be a good solution for a way to select files to process from the server Streamlit is running on.

Here's a pretty functional solution. 

Usage:

```
import streamlit as st
from filepicker import st_file_selector

tif_file = st_file_selector(st, key = 'tif', label = 'Choose tif file')
```
"""

import os

import streamlit as st

i_will_regret_this2 = 0
i_will_regret_this = 0  # TODO: don't use some global var
def update_dir(key,idx):
    global i_will_regret_this, i_will_regret_this2
    choice = st.session_state[key]
    if os.path.isdir(os.path.join(st.session_state[key + "curr_dir"], choice)):
        if idx:
            i_will_regret_this2 = 0
        else:
            i_will_regret_this = 0
        st.session_state[key + "curr_dir"] = os.path.normpath(
            os.path.join(st.session_state[key + "curr_dir"], choice)
        )
        files = sorted(os.listdir(st.session_state[key + "curr_dir"]))
        files.insert(0, "..")
        files.insert(0, ".")
        st.session_state[key + "files"] = files




def st_file_selector(
    st_placeholder, path=".", label="Select a file/folder", key="selected"
):
    if key + "curr_dir" not in st.session_state:
        base_path = "." if path is None or path == "" else path
        base_path = (
            base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
        )
        base_path = "." if base_path is None or base_path == "" else base_path

        files = sorted(os.listdir(base_path))
        files.insert(0, "..")
        files.insert(0, ".")
        st.session_state[key + "files"] = files
        st.session_state[key + "curr_dir"] = base_path
        if os.path.isfile(path):
            global i_will_regret_this
            i_will_regret_this = st.session_state[key + "files"].index(
                os.path.basename(path)
            )
    else:
        base_path = st.session_state[key + "curr_dir"]

    selected_file = st_placeholder.selectbox(
        label=label,
        options=st.session_state[key + "files"],
        index=i_will_regret_this,
        key=key,
        on_change=lambda: update_dir(key,0),
    )
    selected_path = os.path.normpath(os.path.join(base_path, selected_file))
    st_placeholder.write(os.path.abspath(selected_path))

    return selected_path



def st_file_selector2(
    st_placeholder, path=".", label="Select a file/folder", key="selected"
):
    if key + "curr_dir" not in st.session_state:
        base_path = "." if path is None or path == "" else path
        base_path = (
            base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
        )
        base_path = "." if base_path is None or base_path == "" else base_path

        files = sorted(os.listdir(base_path))
        files.insert(0, "..")
        files.insert(0, ".")
        st.session_state[key + "files"] = files
        st.session_state[key + "curr_dir"] = base_path
        if os.path.isfile(path):
            global i_will_regret_this2
            i_will_regret_this2 = st.session_state[key + "files"].index(
                os.path.basename(path)
            )
    else:
        base_path = st.session_state[key + "curr_dir"]

    selected_file = st_placeholder.selectbox(
        label=label,
        options=st.session_state[key + "files"],
        index=i_will_regret_this2,
        key=key,
        on_change=lambda: update_dir(key,1),
    )
    selected_path = os.path.normpath(os.path.join(base_path, selected_file))
    st_placeholder.write(os.path.abspath(selected_path))

    return selected_path