<template>
    <section class="p-md md:p-lg max-w-[1280px] w-full mx-auto space-y-lg">
    <!-- Breadcrumbs -->
        <div class="flex items-center gap-sm text-[#76777d] font-bold text-[11px] uppercase tracking-widest">
            <span>Precision Analytical</span>
            <span class="material-symbols-outlined text-[14px]">chevron_right</span>
            <span class="text-black">Catalog</span>
        </div>
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-md">
            <div class="bg-white border border-[#e5eeff] p-md rounded-lg flex flex-col justify-between">
                <span class="text-[#76777d] text-[11px] font-bold uppercase">Total Active Products</span>
                <div class="flex items-baseline gap-sm mt-sm">
                    <span class="text-display-lg font-bold text-black">1,284</span>
                    <span class="text-[#006a61] text-xs font-bold">+4%</span>
                </div>
            </div>
            <div class="bg-white border border-[#e5eeff] p-md rounded-lg flex flex-col justify-between">
                <span class="text-[#76777d] text-[11px] font-bold uppercase">Avg. Price Stability</span>
                <div class="flex items-baseline gap-sm mt-sm">
                    <span class="text-display-lg font-bold text-black">94.2%</span>
                    <span class="text-[#006a61] text-xs font-bold">Stable</span>
                </div>
            </div>
        </div>
        <!-- Main Table Container -->
        <div class="bg-white border border-[#e5eeff] rounded-lg overflow-hidden shadow-sm">
            <!-- Table Controls -->
            <div class="px-md py-md border-b border-[#eff4ff] flex items-center justify-between">
                <h3 class="font-bold text-lg text-black">Product Catalog</h3>
                <div class="flex items-center gap-sm">
                    <button class="px-md py-sm text-[#76777d] text-sm font-bold border border-[#d3e4fe] rounded-lg flex items-center gap-sm hover:bg-[#eff4ff] transition-colors">
                        <span class="material-symbols-outlined text-sm">filter_list</span>Filter
                    </button>
                    <button class="px-md py-sm bg-[#006a61] text-white text-sm font-bold rounded-lg flex items-center gap-sm hover:opacity-90 transition-opacity">
                        <span class="material-symbols-outlined text-sm">download</span>Export CSV
                    </button>
                </div>
            </div>
            <!-- Product Table -->
            <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
            <thead>
                <tr class="bg-[#eff4ff]">
                    <th class="px-md py-sm font-bold text-[11px] uppercase text-[#76777d] border-b border-[#e5eeff]">
                        <div class="flex items-center gap-xs cursor-pointer">Product Name
                            <span class="material-symbols-outlined text-[16px]">swap_vert</span>
                        </div>
                    </th>
                    <th class="px-md py-sm font-bold text-[11px] uppercase text-[#76777d] border-b border-[#e5eeff]">
                        <div class="flex items-center gap-xs cursor-pointer">
                                                                Current Price
                                                                <span class="material-symbols-outlined text-[16px]">swap_vert</span>
                        </div>
                    </th>
                    <th class="px-md py-sm font-bold text-[11px] uppercase text-[#76777d] border-b border-[#e5eeff]">7-Day Forecast Trend</th>
                    <th class="px-md py-sm font-bold text-[11px] uppercase text-[#76777d] border-b border-[#e5eeff]">
                                                        Status
                                                    </th>
                    <th class="px-md py-sm font-bold text-[11px] uppercase text-[#76777d] border-b border-[#e5eeff] text-right">
                                                        Actions
                                                    </th>
                </tr>
            </thead>
            <tbody class="divide-y divide-[#eff4ff]">
            <!-- Product Row 1 -->
            <tr class="hover:bg-[#f8f9ff] transition-colors group">
            <td class="px-md py-md">
            <div class="flex items-center gap-md">
            <div class="w-10 h-10 rounded bg-[#eff4ff] flex items-center justify-center text-[#76777d]">
            <span class="material-symbols-outlined">memory</span>
            </div>
            <div>
            <p class="font-bold text-black text-sm">Core Processor X1</p>
            <p class="text-[11px] text-[#76777d]">SKU: CP-X1-2024</p>
            </div>
            </div>
            </td>
            <td class="px-md py-md font-medium text-black text-sm">
                                                $429.50
                                            </td>
            <td class="px-md py-md">
            <div class="flex items-center gap-sm">
            <div class="flex items-end gap-[2px] h-6">
            <div class="w-1.5 h-2 bg-[#006a61]/20"></div>
            <div class="w-1.5 h-3 bg-[#006a61]/40"></div>
            <div class="w-1.5 h-4 bg-[#006a61]/60"></div>
            <div class="w-1.5 h-5 bg-[#006a61]/80"></div>
            <div class="w-1.5 h-6 bg-[#006a61]"></div>
            </div>
            <span class="text-[#006a61] text-[11px] font-bold flex items-center">
            <span class="material-symbols-outlined text-[14px]">trending_up</span>
                                                        +2.4%
                                                    </span>
            </div>
            </td>
            <td class="px-md py-md">
            <span class="px-2 py-0.5 bg-[#eff4ff] text-[#006a61] border border-[#d3e4fe] rounded text-[10px] font-bold uppercase tracking-wider">Ascending</span>
            </td>
            <td class="px-md py-md text-right">
            <button class="text-[#76777d] hover:text-black p-1">
            <span class="material-symbols-outlined">more_vert</span>
            </button>
            </td>
            </tr>
            <!-- Product Row 2 -->
            <tr class="hover:bg-[#f8f9ff] transition-colors group">
            <td class="px-md py-md">
            <div class="flex items-center gap-md">
            <div class="w-10 h-10 rounded bg-[#eff4ff] flex items-center justify-center text-[#76777d]">
            <span class="material-symbols-outlined">storage</span>
            </div>
            <div>
            <p class="font-bold text-black text-sm">Solid State Drive 2TB</p>
            <p class="text-[11px] text-[#76777d]">SKU: SSD-2TB-PRO</p>
            </div>
            </div>
            </td>
            <td class="px-md py-md font-medium text-black text-sm">
                                                $185.00
                                            </td>
            <td class="px-md py-md">
            <div class="flex items-center gap-sm">
            <div class="flex items-end gap-[2px] h-6">
            <div class="w-1.5 h-6 bg-error/80"></div>
            <div class="w-1.5 h-4 bg-error/60"></div>
            <div class="w-1.5 h-2 bg-error/40"></div>
            <div class="w-1.5 h-1 bg-error/20"></div>
            </div>
            <span class="text-error text-[11px] font-bold flex items-center">
            <span class="material-symbols-outlined text-[14px]">trending_down</span>
                                                        -1.1%
                                                    </span>
            </div>
            </td>
            <td class="px-md py-md">
            <span class="px-2 py-0.5 bg-error/10 text-error border border-error/20 rounded text-[10px] font-bold uppercase tracking-wider">Correction</span>
            </td>
            <td class="px-md py-md text-right">
            <button class="text-[#76777d] hover:text-black p-1">
            <span class="material-symbols-outlined">more_vert</span>
            </button>
            </td>
            </tr>
            <!-- Product Row 3 -->
            <tr class="hover:bg-[#f8f9ff] transition-colors group">
            <td class="px-md py-md">
            <div class="flex items-center gap-md">
            <div class="w-10 h-10 rounded bg-[#eff4ff] flex items-center justify-center text-[#76777d]">
            <span class="material-symbols-outlined">cable</span>
            </div>
            <div>
            <p class="font-bold text-black text-sm">Optical Fiber Bundle</p>
            <p class="text-[11px] text-[#76777d]">SKU: OFB-100-ST</p>
            </div>
            </div>
            </td>
            <td class="px-md py-md font-medium text-black text-sm">
                                                $89.99
                                            </td>
            <td class="px-md py-md">
            <div class="flex items-center gap-sm">
            <div class="flex items-end gap-[2px] h-2">
            <div class="w-1.5 h-2 bg-[#d3e4fe]"></div>
            <div class="w-1.5 h-2 bg-[#d3e4fe]"></div>
            <div class="w-1.5 h-2 bg-[#d3e4fe]"></div>
            <div class="w-1.5 h-2 bg-[#d3e4fe]"></div>
            </div>
            <span class="text-[#76777d] text-[11px] font-bold flex items-center">
            <span class="material-symbols-outlined text-[14px]">trending_flat</span>
                                                        0.0%
                                                    </span>
            </div>
            </td>
            <td class="px-md py-md">
            <span class="px-2 py-0.5 bg-[#eff4ff] text-[#76777d] border border-[#d3e4fe] rounded text-[10px] font-bold uppercase tracking-wider">Stable</span>
            </td>
            <td class="px-md py-md text-right">
            <button class="text-[#76777d] hover:text-black p-1">
            <span class="material-symbols-outlined">more_vert</span>
            </button>
            </td>
            </tr>
            </tbody>
            </table>
            </div>
            <!-- Table Footer -->
            <div class="px-md py-sm border-t border-[#eff4ff] flex items-center justify-between text-[#76777d] text-[11px] font-bold uppercase">
            <p>Showing 1 to 3 of 1,284 products</p>
            <div class="flex items-center gap-xs">
            <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-[#eff4ff]">
            <span class="material-symbols-outlined text-[18px]">chevron_left</span>
            </button>
            <button class="w-8 h-8 flex items-center justify-center rounded bg-[#006a61] text-white">1</button>
            <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-[#eff4ff]">2</button>
            <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-[#eff4ff]">3</button>
            <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-[#eff4ff]">
            <span class="material-symbols-outlined text-[18px]">chevron_right</span>
            </button>
            </div>
            </div>
        </div>
    </section>
</template>