<template>
  <div class="container flex justify-center">
    <div class="basis-1/4">
      <h1 class="text-2xl my-4 text-zinc-900 font-semibold">Login</h1>
      <form>
        <div>
          <label class="block text-xs font-medium text-zinc-500" for="login-email">Email</label>
          <div class="mt-1">
            <input required class="border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400" id="login-email" type="email" placeholder="you@company.com">
          </div>
        </div>
        <div class="mt-2">
          <label class="block text-xs font-medium text-zinc-500" for="login-password">Password</label>
          <div class="mt-1">
            <input required class="border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400" id="login-password" type="password" placeholder="Password">
          </div>
        </div>
        <div class="mt-3">
          <button type="submit" class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Login</button>
          <NuxtLink to="/register"><small class="ml-2 text-green-500 hover:text-green-700">or register here.</small></NuxtLink>
        </div>
      </form>
    </div>
  
  </div>
</template>