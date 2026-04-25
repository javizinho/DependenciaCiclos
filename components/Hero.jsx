'use client'
import { assets } from '@/assets/assets'
import { ArrowRightIcon, ChevronRightIcon } from 'lucide-react'
import Image from 'next/image'
import React from 'react'
import CategoriesMarquee from './CategoriesMarquee'

const Hero = () => {

    const currency = process.env.NEXT_PUBLIC_CURRENCY_SYMBOL || '$'

    return (
        <div className='mx-6'>
            <div className='flex max-xl:flex-col gap-8 max-w-7xl mx-auto my-10'>
                
                {/* TARJETA PRINCIPAL: TECNOLOGÍA */}
                <div className='relative flex-1 flex flex-col bg-gradient-to-br from-[#DDEBFF] via-[#F1F7FF] to-[#FFFFFF] shadow-[0_20px_50px_rgba(59,130,246,0.12)] border border-blue-100/50 rounded-[2.5rem] xl:min-h-[500px] overflow-hidden group'>
                    
                    {/* Contenido de Texto: Z-10 para estar siempre al frente */}
                    <div className='p-8 sm:p-16 z-10 relative flex flex-col items-start'>
                        
                        {/* Badge */}
                        <div className='inline-flex items-center gap-3 bg-blue-100/80 backdrop-blur-sm text-[#2563EB] pr-4 p-1 rounded-full text-xs sm:text-sm border border-blue-200'>
                            <span className='bg-[#2563EB] px-3 py-1 max-sm:ml-1 rounded-full text-white text-xs font-bold shadow-sm'>PRÓXIMAMENTE</span> 
                            <span className='hidden sm:inline font-medium'>Con Aima Plus tendrás descuentos únicos!</span>
                            <ChevronRightIcon className='group-hover:translate-x-1 transition-all' size={16} />
                        </div>

                        {/* Título con degradado limpio */}
                        <h2 className='text-3xl sm:text-5xl leading-[1.2] my-5 font-bold bg-gradient-to-r from-[#0F172A] via-[#1E40AF] to-[#3B82F6] bg-clip-text text-transparent max-w-xs sm:max-w-sm'>
                            Innovación, Aroma y Pasión.
                        </h2>

                        {/* Precio */}
                        <div className='text-slate-700 text-sm font-medium mt-4'>
                            <p>Precios desde</p>
                            <p className='text-4xl font-black text-[#0F172A] tracking-tight'>{currency}4.90</p>
                        </div>

                        {/* Botón */}
                        <button className='bg-[#3B82F6] text-white text-sm font-bold py-4 px-12 mt-10 rounded-xl shadow-[0_10px_25px_rgba(59,130,246,0.3)] hover:bg-[#2563EB] hover:scale-105 active:scale-95 transition-all duration-300 uppercase tracking-widest'>
                            LEER MÁS
                        </button>
                    </div>

                    {/* IMAGEN CORREGIDA: Ajuste de posición y tamaño para que no tape el texto */}
                    <div className='absolute bottom-0 right-0 w-[55%] sm:w-[50%] lg:w-[55%] max-w-[500px] pointer-events-none select-none'>
                        <Image 
                            className='w-full h-auto object-contain object-right-bottom transition-transform duration-700 group-hover:scale-105 group-hover:-translate-y-2 drop-shadow-[-20px_20px_30px_rgba(0,0,0,0.1)]' 
                            src={assets.hero_model_img} 
                            alt="Tecnología Aima Store" 
                            priority
                        />
                    </div>
                </div>

                {/* COLUMNA DERECHA: TARJETAS SECUNDARIAS */}
                <div className='flex flex-col md:flex-row xl:flex-col gap-5 w-full xl:max-w-sm text-sm'>
                    
                    {/* Tarjeta Fragancias: Ámbar/Oro */}
                    <div className='flex-1 flex items-center justify-between w-full bg-gradient-to-br from-[#FFF7ED] via-[#FFEDD5] to-[#FED7AA] rounded-[2rem] p-8 group border border-orange-100 shadow-[0_15px_40px_rgba(251,146,60,0.1)] overflow-hidden relative'>
                        <div className='z-10 relative'>
                            <p className='text-2xl font-bold bg-gradient-to-br from-[#451A03] to-[#B45309] bg-clip-text text-transparent max-w-[140px] leading-tight'>
                                Explora fragancias únicas.
                            </p>
                            <p className='flex items-center gap-1 mt-6 font-bold text-[#92400E] cursor-pointer group-hover:translate-x-2 transition-all'>
                                Ver más <ArrowRightIcon size={18} /> 
                            </p>
                        </div>
                        <Image 
                            className='w-28 sm:w-32 z-0 transition-transform duration-500 group-hover:scale-110 group-hover:rotate-6 drop-shadow-2xl' 
                            src={assets.hero_product_img1} 
                            alt="Perfumes" 
                        />
                    </div>

                    {/* Tarjeta Indumentaria (Efecto Cristal/Glaciar) */}
                    <div className='flex-1 flex items-center justify-between w-full bg-gradient-to-br from-[#E0F2FE] via-[#F0F9FF] to-[#FFFFFF] rounded-[2rem] p-8 group border border-sky-100/50 shadow-[0_15px_40px_rgba(56,189,248,0.1)] overflow-hidden relative'>
                        <div className='z-10 relative'>
                            <p className='text-2xl font-bold bg-gradient-to-br from-[#0F172A] to-[#0369A1] bg-clip-text text-transparent max-w-[140px] leading-tight'>
                                Viste los colores que amas.
                            </p>
                            <p className='flex items-center gap-1 mt-6 font-bold text-[#0284C7] cursor-pointer group-hover:translate-x-2 transition-all'>
                                Ver más <ArrowRightIcon size={18} /> 
                            </p>
                        </div>
                        {/* Imagen de la camiseta con una sombra profunda para que parezca flotar */}
                        <Image className='w-28 sm:w-32 z-0 transition-transform duration-500 group-hover:scale-110 group-hover:-rotate-3 drop-shadow-2xl' src={assets.hero_product_img2} alt="Indumentaria Argentina" />
                    </div>

                </div>
            </div>
            <CategoriesMarquee />
        </div>
    )
}

export default Hero