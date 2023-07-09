import { reactive } from 'vue'

const store = reactive({
    token: localStorage.getItem("token"),
    profile: {
        first_name: '',
        last_name: '',
        picture_url: '',
        email: '',
    }
});

export { store }
