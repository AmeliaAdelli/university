/*
Напишите программу, обрабатывающую стандартный поток ввода 
и выводящую результат на стандартный поток вывода. 
Программа заменяет все цифры '0' ... '9' на цифру '0'. 
Все остальные символы во входном потоке не изменяются.
*/
#include <asm/unistd_32.h>
	.text
	.global	_start
_start:
	subl	$4, %esp
scan:
	movl	$__NR_read,	%eax
	movl	$0,	%ebx
	movl	%esp,	%ecx
	movl	$1,	%edx
	int	$0x80

	cmpl	$0,	%eax
	je	end

	cmpl	$'0',	(%esp)
	jnl	check_if_number
	jmp	print
check_if_number:
	cmpl	$'9',	(%esp)
	jg	print
	movl	$'0',	(%esp)
print:
	movl	$__NR_write,	%eax
	movl	$1,	%ebx
	movl	%esp,	%ecx
	movl	$1,	%edx
	int	$0x80
	jmp	scan
end:
	movl	$__NR_exit,	%eax
	movl	$0,	%ebx
	int	$0x80
