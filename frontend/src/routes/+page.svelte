<script lang="ts">
	import pigeon from '$lib/images/pigeon.webp';
	import { onMount } from 'svelte';

	let files = <any>[];

	onMount(async () => {
		const response = await fetch('http://127.0.0.1:8000/files');
		const { files: data } = await response.json();
		files = data;
	});

	const download = (id: Number) => async () => {
		console.log(id);
		const response = await fetch(`http://127.0.0.1:8000/files/${id}`);
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
		<input type="file" />
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
				<div on:click={download(file.id)}>
					<h2>get</h2>
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
		grid-template-columns: 10fr 10fr 10fr 1fr;
	}
</style>
