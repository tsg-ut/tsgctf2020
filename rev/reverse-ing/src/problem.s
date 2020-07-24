BITS 64

; nasm tes.s -felf64 -o tes.o && ld tes.o && strip -N loop a.out
section .txt progbits alloc exec write align=16

reverse:
	pushf
	push rdi
	push rsi
	push rdx
	push rcx
	push rbx
	mov rcx,106
revloop:
	xor rdi,rdi
	mov edi,_start
	add rdi,rcx
	xor rsi,rsi
	mov esi,end
	sub rsi,rcx
	mov dl,[rdi]
	mov bl,[rsi]
	mov [rsi],dl
	mov [rdi],bl
	dec rcx
	jns revloop
	pop rbx
	pop rcx
	pop rdx
	pop rsi
	pop rdi
	popf
	ret

global _start
_start:
	xor rbx,rbx
	mov ebx,reverse
	call rbx
	xor rdx,rdx
	call rbx
	mov dl,0x25
	call rbx
	mov rsi,rsp
	call rbx
	xor rdi,rdi
	call rbx
	xor rax,rax
	call rbx
	syscall
	call rbx
	dec rdx
	call rbx
	xor rcx,rcx
	call rbx
loop:
	mov cl,[rsi+rdx]
	call rbx
	xor cl,[key1+rdx] ; upright
	call rbx
	add cl,[key1+rdx] ; downright
	call rbx
	or rdi,rcx
	call rbx
	dec dl
	call rbx
	jns loop2
	call rbx
	mov dl,8
	call rbx
	mov al,1
	call rbx
	xor rsi,rsi
	call rbx
	mov esi,correct
	call rbx
	dec edi
	call rbx
	call rbx
	js ok
	call rbx
	mov esi,wrong
	call rbx
ok:
	xor rdi,rdi
	call rbx
	inc edi
	call rbx
	syscall
	call rbx
	mov al,60
	call rbx
	syscall
	call rbx
loop2:
	mov cl,[rsi+rdx]
	call rbx
	xor cl,[key1+rdx] ; down
	call rbx
	add cl,[key1+rdx]
	call rbx
	or rdi,rcx
	call rbx
	sub dl,1
	call rbx
	jns loop
	call rbx

key1:
	resb 38
end:
	db 0x0
correct:
	db "correct",10
wrong:
	db "wrong",10, 0, 0

section .note.GNU-stack noalloc noexec nowrite progbits
