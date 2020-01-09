(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.

(define (cons-all first rests)
  (map (lambda (x) (cons first x)) rests)
  )

(define (zip pairs)
  (cons (map (lambda (x) (car x)) pairs) 
        (list (map (lambda (x) (car (cdr x))) pairs)))
  )

;; Problem 16
;; Returns a list of two-element lists
(define (enumerate s)
  (define (enumerate_helper s c)
      (if (null? s) nil
        (begin
            (define sub_list (cons c (cons (car s) nil)))
            (cons sub_list (enumerate_helper (cdr s) (+ c 1)))
      )
    
      )
  )
  (enumerate_helper s 0)
  )
  ; END PROBLEM 16

;; Problem 17
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
    (if (not(null? denoms))
            (define coin (car denoms))
    )
    (cond 
        ((null? denoms) nil)
        ((< total 0) nil)
        ((= total 0) 
            (list (list coin)))
        ((> total coin) 
            (append (cons-all coin (list-change (- total coin) denoms)) (list-change total (cdr denoms))))
        ((< total coin)
            (list-change total (cdr denoms)))
        (else
            (append (list-change (- total coin) denoms) (list-change total (cdr denoms)))
        )
    )
)
  

  ; END PROBLEM 17

;; Problem 18
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         expr
         )
        ((quoted? expr)
         expr)
         
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))


             (append (list form params) (map let-to-lambda body) )
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           (define params (car (zip values)))
           (define body (map let-to-lambda body))
           (define arguements (map let-to-lambda (cadr (zip values))))
           
           (cons (append (list 'lambda params) body)
                 arguements)
           ))
        (else
         (append (list (car expr)) (map let-to-lambda (cdr expr)))
         )))
     
     
(let-to-lambda '(let ((a 1)
            (b 2))
            (+ a b)))