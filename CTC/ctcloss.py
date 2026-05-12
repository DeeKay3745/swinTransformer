import torch

NEF_INF = torch.finfo(torch.float32).min
def ctc_loss(log_probs, targets, input_lengths, target_lengths, blank =0, reduction="none"):
    # ex: targets [28,1,17,21]
    # log_probs.shape-> (T X BX C)
    #input_lengths.shape  ->(B,)
    #target_lengths.shape->(B,)
    seq_len, batch_size, num_classes = log_probs.shape
    B = torch.arange(batch_size)
    # _t_a_r_g_e_t_s_:[28,1,17,21,0] -> Append a blank token at the end (we could really use anything, doent matter)
    # its just a placeholder so our indexing is happy , we will never this token anywhere or include it in the loss
    _t_a_r_g_e_t_s_ = torch.cat([targets, torch.zeros(batch_size, 1, device = log_probs.device, dtype=torch.long)], dim=-1)
    #print(_t_a_r_g_e_t_s_)
    # _t_a_r_g_e_t_s_ : [0,28,0,1,0,17,0,21,0,0]-> Insert blank tokens in between targets
    _t_a_r_g_e_t_s_ = torch.stack([torch.full_like(_t_a_r_g_e_t_s_, blank), _t_a_r_g_e_t_s_], dim =-1).flatten(start_dim=-2)
    diff_labels = torch.cat([torch.tensor([[False, False]], device = log_probs.device).expand(batch_size, -1),
                                          (_t_a_r_g_e_t_s_[:, :-2] != _t_a_r_g_e_t_s_[:,2:])], dim=-1)
    #print(diff_labels.shape, _t_a_r_g_e_t_s_.shape)
    index =_t_a_r_g_e_t_s_.expand(seq_len, -1, -1)
    log_probs_ = log_probs.gather(dim= -1, index = index )
    #print(log_probs.shape)

    log_alpha = torch.full((seq_len, batch_size, 2+_t_a_r_g_e_t_s_.shape[-1]), NEF_INF).to(device)
    log_alpha[0, :, 2] = log_probs[0,:,blank]
    log_alpha[0,:,2+1] = log_probs[0,B,_t_a_r_g_e_t_s_[:,1]]
    for T_ in range(1,T):
        log_probs_T_ = log_probs_[T_]
        #print(log_probs_T_)
        log_alpha_T_prev_stay = log_alpha[T_-1,:,2:]
        log_alpha_T_prev_next = log_alpha[T_-1,: ,1:-1]
        log_alpha_two_step_transition = torch.where(diff_labels, input = log_alpha[T_-1, :,:-2], other=NEF_INF)
        prob = torch.logsumexp(torch.stack([log_alpha_T_prev_next,log_alpha_T_prev_stay, log_alpha_two_step_transition]), dim=0)
        log_alpha[T_,:,2:] = log_probs_T_+ prob
    #print(log_alpha)
    final_log_alpha = log_alpha[input_lengths-1,B]
    #print(final_log_alpha)
    ending_on_label_index = 2+target_lengths *2-1
    ending_on_blank_index = 2 + target_lengths * 2
    indexs_to_grab = torch.stack([ending_on_label_index, ending_on_blank_index], dim=-1) 
    #print(indexs_to_grab)
    label_or_blank_ending_log_alphas = final_log_alpha.gather(dim =-1, index= indexs_to_grab)
    #print(label_or_blank_ending_log_alphas)
    loss = - torch.logsumexp(label_or_blank_ending_log_alphas,dim =-1)
    if reduction=="none":
        return loss
    elif reduction =="sum":
        return torch.sum(loss)
    elif reduction =="mean":
        return torch.mean(loss)
        #[PAD PAD, A,B,C,D,E]
        #[A,B,C,D,E]
        #[PAD, A,B,C,D]
        #[PAD PAD, A,B,C] */


if __name__ =="__main__":
    T, B, C = 128, 1, 32
    t =50
    blank =0 
    device = "cuda" if torch.cuda.is_available() else "cpu"
    atol =1e-3

    logits = torch.randn(T,B, C).requires_grad_().to(device)
    log_probs =logits.log_softmax(dim =-1).to(device)
    targets = torch.randint(1,C,(B,t), dtype=torch.long).to(device)
    input_lengths = torch.full((B,),T, dtype=torch.long).to(device)
    target_lengths =torch.full((B,), t, dtype=torch.long).to(device)
    torch_ctc = torch.nn.functional.ctc_loss(log_probs,targets, input_lengths, target_lengths, blank =0 , reduction = 'none')
    torch_ctc_grad, = torch.autograd.grad(torch_ctc.mean(), logits, retain_graph =True)
    my_ctc =ctc_loss(log_probs= log_probs, targets=targets, input_lengths= input_lengths, target_lengths= target_lengths)
    my_ctc_grad, = torch.autograd.grad(my_ctc.mean(), logits, retain_graph =True)
    print("CTC losses Match:", torch.allclose(torch_ctc, my_ctc, atol = atol))
    print("Grad matches:", torch.allclose(torch_ctc_grad, my_ctc_grad, atol = atol))