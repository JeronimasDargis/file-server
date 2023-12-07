import { apiUrl } from '../constants';
import { routes } from '../routes';

const getAllFiles = async () => {
	try {
		const response = await fetch(`${apiUrl}${routes.files}`);
		const { files: data } = await response.json();
		return data;
	} catch (error) {
		console.error('Error fetching posts:', error);
		throw error;
	}
};

// @todo figure out why the name is not being passed from the backend and fix this temp solution
const downloadFile = async (fileId: number) => {
	const downloadUrl = `${apiUrl}${routes.download}/${fileId}`;
	const link = document.createElement('a');
	link.href = downloadUrl;
	link.click();
};

const deleteFile = async (fileId: number) => {
	try {
		const response = await fetch(`${apiUrl}${routes.delete}/${fileId}`, {
			method: 'POST'
		});

		if (!response.ok) {
			throw new Error(`Error deleting file ${response.status}`);
		}

		const data = await response.json();
		console.log('Success:', data);
	} catch (error) {
		// Handle errors here
		console.error('Error:', error.message);
	}
};

const uploadFile = async (form, formData: FormData) => {
	await fetch(form.action, {
		method: form.method,
		body: formData
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.catch((error) => {
			console.error('There was a problem with the file upload:', error);
		});
};

export { getAllFiles, downloadFile, deleteFile, uploadFile };
