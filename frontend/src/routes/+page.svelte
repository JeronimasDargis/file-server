<script lang="ts">
	import pigeon from '$lib/images/pigeon.webp';
	import { apiUrl } from '../api/constants';
	import { routes } from '../api/routes';
	import { onMount } from 'svelte';
	import { getAllFiles, downloadFile, deleteFile, uploadFile } from '../api/files';

	let files = <any>[];

	onMount(async () => {
		const response = await getAllFiles();
		files = response;
	});

	async function triggerFileUpload() {
		const form = document.getElementById('uploadForm') as HTMLFormElement;
		const formData = new FormData(form);
		uploadFile(form, formData);
	}
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
			on:submit|preventDefault={triggerFileUpload}
			id="uploadForm"
			action="{apiUrl}{routes.upload}"
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

	.file-row {
		background-color: azure;
		padding: 0.5rem;
		border-radius: 0.5rem;
		display: grid;
		grid-template-columns: 10fr 10fr 8fr 1fr;
		margin-bottom: 0.5rem;
	}
</style>
