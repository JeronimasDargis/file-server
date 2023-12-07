<script lang="ts">
	import pigeon from '$lib/images/pigeon.webp';
	import { onMount } from 'svelte';

	let files = <any>[];

	onMount(async () => {
		const response = await fetch('http://192.168.1.104:8080/files');
		const { files: data } = await response.json();
		files = data;

		const fileUploadInput = document.getElementById('uploadForm');
		if (fileUploadInput) {
			fileUploadInput.addEventListener('submit', uploadFile());
		}
	});

	function downloadFile(id: Number) {
		const downloadUrl = `http://192.168.1.104:8080/download/${id}`;
		const link = document.createElement('a');
		link.href = downloadUrl;
		link.click();
	}

	const deleteFile = (id: Number) => async () => {
		const response = await fetch(`http://192.168.1.104:8080/delete/${id}`, {
			method: 'POST'
		});
		console.log(response);
	};

	const uploadFile = () => async (e: Event) => {
		e.preventDefault(); // Prevent the default form submission behavior

		const form = document.getElementById('uploadForm') as HTMLFormElement;
		const formData = new FormData(form);

		fetch(form.action, {
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
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="my home" />
</svelte:head>

<section>
	<div class="section">
		<img style="width: auto; padding-bottom: 2rem; height: 300px;" src={pigeon} alt="Pigeon" />
		<h1>Give me your files</h1>
		<form
			id="uploadForm"
			action="http://192.168.1.104:8080/upload"
			method="post"
			enctype="multipart/form-data"
		>
			<input type="file" name="file" />
			<input type="submit" value="Upload" />
		</form>
	</div>

	<div class="collection">
		<div style="display: grid; grid-template-columns: 10fr 10fr 10fr 1fr; padding: 0.5rem">
			<p>name</p>
			<p>uploaded</p>
			<p>size</p>
		</div>
		{#each files as file}
			<div class="file-row">
				<h2>
					{file.filename}
				</h2>
				<h2>
					{file.upload_date}
				</h2>
				<h2>size..</h2>
				<div style="display: flex">
					<button on:click={downloadFile(file.id)}>
						<h2>get</h2>
					</button>
					<button on:click={deleteFile(file.id)}>
						<h2>delete</h2>
					</button>
				</div>
			</div>
		{:else}
			<p>loading...</p>
		{/each}
	</div>
</section>

<style>
	.section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
		margin-bottom: 5rem;
	}

	.collection {
		/* styling */
	}

	.file-row {
		background-color: azure;
		padding: 0.5rem;
		border-radius: 0.5rem;
		display: grid;
		grid-template-columns: 10fr 10fr 8fr 1fr;
		margin-bottom: 0.5rem;
	}
</style>
