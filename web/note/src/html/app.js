function api(path, body, method = 'POST') {
    return fetch(path, {
        method,
        credentials: 'include',
        ...(method == 'POST' ? {
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        } : {}),
    }).then(res => {
        if(!res.ok) {
            return res.json().catch(_ => {
                throw {message: 'something went wrong'};
            }).then(({message}) => {
                throw {message: message || 'something went wrong'};
            });
        }
        return res;
    });
}

const app = new Vue({
    el: '#app',
    data: {
        tab: 'transfer',
        headerImg: document.location.hash.substring(1) || '',
        search: document.location.search.substring(1) || '',
        editingNote: '',
        allNotes: [],
        visibleNotes: [],
        loggedin: false,
    },
    watch: {
        search() {
            this.updateVisibleNotes();
        },
        allNotes() {
            this.updateVisibleNotes();
            console.log(this.allNotes.length);
        },
    },
    mounted() {
        this.updateNotes();
    },
    methods: {
        async updateNotes() {
            try {
                const notes = await (await api('/api/note', '', 'GET')).json();
                this.loggedin = true;
                console.log(notes);
                this.allNotes = notes;
            } catch {
                this.loggedin = false
                this.allNotes = [];
            };
        },
        async updateVisibleNotes() {
            try {
                const re = new RegExp(this.search);
                this.visibleNotes = this.allNotes.filter(({content}) => content.match(re));
            } catch {
                // pass
            }
        },
        async register() {
            await api('/api/register', {});
            await this.updateNotes();
        },
        async logout() {
            await api('/api/logout', {})
            this.updateNotes();
        },
        async postNote() {
            await api('/api/note', {note: this.editingNote});
            this.editingNote = '';
            const notes = await (await api('/api/note', '', 'GET')).json();
            this.allNotes = notes;
        },
        async deleteNote(ev) {
            const e = ev.target;
            const noteid = e.getAttribute('noteid');
            await api(`/api/note/${noteid}`, {}, 'DELETE');
            const notes = await (await api('/api/note', '', 'GET')).json();
            this.allNotes = notes;
        },
    }
});
